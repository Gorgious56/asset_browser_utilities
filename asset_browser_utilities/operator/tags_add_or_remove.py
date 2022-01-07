import os.path
import functools
import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, PointerProperty

from asset_browser_utilities.prop.path import LibraryExportSettings
from asset_browser_utilities.prop.filter_settings import AssetFilterSettings
from asset_browser_utilities.prop.tag_collection import TagCollection
from asset_browser_utilities.helper.path import get_blend_files


class ASSET_OT_export(Operator, ImportHelper):
    bl_idname = "asset.tags_add_or_remove"
    bl_label = "Execute"

    filter_glob: StringProperty(
        default="*.blend",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    overwrite: BoolProperty(
        default=True,
        name="Overwrite Tags",
        description="If the tag already exists on the asset, do not create a new one",
    )
    add: BoolProperty()

    library_export_settings: PointerProperty(type=LibraryExportSettings)
    asset_filter_settings: PointerProperty(type=AssetFilterSettings)
    tag_collection: PointerProperty(type=TagCollection)

    def invoke(self, context, event):
        self.tag_collection.init(tags=10)
        if self.library_export_settings.this_file_only:
            self.asset_filter_settings.init(filter_selection=True)
            return context.window_manager.invoke_props_dialog(self)
        else:
            self.asset_filter_settings.init(filter_selection=False)
            context.window_manager.fileselect_add(self)
            return {"RUNNING_MODAL"}

    def execute(self, context):
        if bpy.data.is_saved and bpy.data.is_dirty:
            bpy.ops.wm.save_mainfile()
        blends = get_blend_files(self)
        for blend in blends:            
            if bpy.data.filepath != str(blend):
                bpy.ops.wm.open_mainfile(filepath=str(blend))

            objs = self.asset_filter_settings.query()
            for obj in objs:
                asset = obj.asset_data
                asset_tags = asset.tags
                if self.add:
                    existing_tags = [tag.name for tag in asset_tags]
                    for tag in self.tag_collection.items:
                        if tag.name == "" or (self.overwrite and tag.name in existing_tags):
                            continue
                        asset_tags.new(tag.name)
                else:
                    tags_to_remove = [tag.name for tag in self.tag_collection.items if tag.name != ""]
                    for i in range(len(asset_tags) - 1, -1, -1):
                        if asset_tags[i].name in tags_to_remove:
                            asset_tags.remove(asset_tags[i])
            
            bpy.ops.wm.save_as_mainfile(filepath=str(blend))

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        self.library_export_settings.draw(layout)
        self.tag_collection.draw(layout)
        self.asset_filter_settings.draw(layout)
