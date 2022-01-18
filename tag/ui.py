from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.helper import is_library


class ABU_MT_tags(Menu):
    bl_label = "Tags"

    def draw(self, context):
        layout = self.layout
        this_file_only = not is_library(context)
        add_tags_op = layout.operator("asset.batch_add_tags", text="Add", icon="ADD")
        add_tags_op.library_settings.this_file_only = this_file_only
        remove_tags_op = layout.operator("asset.batch_remove_tags", text="Remove", icon="REMOVE")
        remove_tags_op.library_settings.this_file_only = this_file_only
