from bpy.types import Menu
from asset_browser_utilities.library.prop import LibraryType


class ABU_MT_tags(Menu):
    bl_label = "Tags"

    def draw(self, context):
        layout = self.layout
        this_file_only = LibraryType.get(context)
        add_tags_op = layout.operator("asset.batch_add_tags", text="Add", icon="ADD")
        add_tags_op.library_settings.this_file_only = this_file_only
        remove_tags_op = layout.operator("asset.batch_remove_tags", text="Remove", icon="REMOVE")
        remove_tags_op.library_settings.this_file_only = this_file_only
