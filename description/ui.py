from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.helper import is_library


class ABU_MT_description(Menu):
    bl_label = "Description"

    def draw(self, context):
        this_file_only = not is_library(context)
        mark_op = self.layout.operator("asset.batch_set_description", text="Set", icon="ADD")
        mark_op.library_settings.this_file_only = this_file_only
