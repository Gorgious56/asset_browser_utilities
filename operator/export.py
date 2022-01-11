import os.path
import functools
import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, EnumProperty, PointerProperty

from asset_browser_utilities.prop.filter.settings import AssetFilterSettings
from asset_browser_utilities.helper.path import (
    is_this_current_file,
    save_if_possible_and_necessary,
    create_new_file_and_set_as_current,
)


class ASSET_OT_export(Operator, ExportHelper):
    bl_idname = "asset.export"
    bl_label = "Export Assets"

    filter_glob: StringProperty(
        default="*.blend",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    filename_ext = ".blend"

    asset_filter_settings: PointerProperty(type=AssetFilterSettings)

    def invoke(self, context, event):
        self.asset_filter_settings.init(filter_selection=True, filter_assets=True)
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        filepath = self.filepath
        if is_this_current_file(filepath):
            return {"FINISHED"}
        source_file = bpy.data.filepath
        save_if_possible_and_necessary()

        assets = self.asset_filter_settings.get_objects_that_satisfy_filters()

        asset_names = [a.name for a in assets]
        asset_types = [type(a).__name__ for a in assets]

        if os.path.isfile(filepath):
            bpy.ops.wm.open_mainfile(filepath=filepath)
        else:
            create_new_file_and_set_as_current(filepath)

        del assets  # Don't keep this in memory since it has been invalidated by loading a new file
        for name, _type in zip(asset_names, asset_types):
            bpy.app.timers.register(
                functools.partial(
                    append_object_from_source,
                    os.path.join(source_file, _type, name),
                    os.path.join(source_file, _type),
                    name,
                ),
                first_interval=0.1,
            )  # Have to delay a bit else context is incorrect
        bpy.ops.wm.save_mainfile()

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout

        self.asset_filter_settings.draw(layout)


def append_object_from_source(filepath, directory, filename):
    bpy.ops.wm.append(filepath=filepath, directory=directory, filename=filename)
