import os.path
from pathlib import Path
import functools
import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator, PropertyGroup
from bpy.props import StringProperty, BoolProperty, EnumProperty, PointerProperty

from asset_browser_utilities.prop.filter.settings import AssetFilterSettings
from asset_browser_utilities.helper.path import (
    is_this_current_file,
    save_if_possible_and_necessary,
    create_new_file_and_set_as_current,
    save_file,
)
from asset_browser_utilities.ui.message import message_box


class ExportProperties(PropertyGroup):
    individual_files: BoolProperty(
        name="Export to Individual Files",
        description="If this is ON, each asset will be exported to an individual file in the target directory",
    )
    prevent_backup: BoolProperty(
        name="Remove Backup",
        description="Check to automatically delete the creation of backup files when 'Save Versions' is enabled in the preferences\nThis will prevent duplicating files when they are overwritten\nWarning : Backup files ending in .blend1 will be deleted permantently",
        default=True,
    )

    def draw(self, layout):
        layout.prop(self, "individual_files")
        layout.prop(self, "prevent_backup", icon="TRASH")


class ASSET_OT_export(Operator, ExportHelper):
    bl_idname = "asset.export"
    bl_label = "Export Assets"

    filter_glob: StringProperty(
        default="*.blend",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    filename_ext = ".blend"

    operator_settings: PointerProperty(type=ExportProperties)
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
        del assets  # Don't keep this in memory since it will be invalidated by loading a new file

        if self.operator_settings.individual_files:
            folder = Path(filepath).parent
            operator_logic = OperatorLogic(
                asset_names, asset_types, source_file, folder, self.operator_settings.prevent_backup
            )
            operator_logic.execute_next()
            return {"FINISHED"}
        else:
            if os.path.isfile(filepath):
                bpy.ops.wm.open_mainfile(filepath=filepath)
            else:
                create_new_file_and_set_as_current(filepath)

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
        save_file(prevent_backup=self.operator_settings.prevent_backup)

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        self.operator_settings.draw(layout)
        self.asset_filter_settings.draw(layout)


class OperatorLogic:
    def __init__(self, asset_names, asset_types, source_file, target_folder, prevent_backup):
        self.asset_names = asset_names
        self.asset_types = asset_types
        self.current_asset_name = ""
        self.current_asset_type = ""

        self.source_file = source_file
        self.target_folder = target_folder

        self.prevent_backup = prevent_backup

    def execute_next(self):
        if self.current_asset_name == "":
            if not self.asset_names:
                message_box(message="Work completed !")
                return
            self.current_asset_name = self.asset_names.pop(0)
            self.current_asset_type = self.asset_types.pop(0)
        new_filepath = os.path.join(self.target_folder, self.current_asset_name + ".blend")
        if os.path.isfile(new_filepath):
            bpy.ops.wm.open_mainfile(filepath=new_filepath)
        else:
            create_new_file_and_set_as_current(new_filepath)

        bpy.app.timers.register(self.append_asset_and_save_file, first_interval=0.1)

    def append_asset_and_save_file(self):
        self.append_asset()
        save_file(remove_backup=self.prevent_backup)
        self.current_asset_name = ""
        self.current_asset_type = ""
        self.execute_next()

    def append_asset(self):
        append_object_from_source(
            os.path.join(self.source_file, self.current_asset_type, self.current_asset_name),
            os.path.join(self.source_file, self.current_asset_type),
            self.current_asset_name,
        )


def append_object_from_source(filepath, directory, filename):
    bpy.ops.wm.append(filepath=filepath, directory=directory, filename=filename)
