from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.helper import is_library


class ABU_MT_author(Menu):
    bl_label = "Author"

    def draw(self, context):
        layout = self.layout
        mark_op = layout.operator("asset.batch_set_author", text="Set", icon="ADD")
        mark_op.library_settings.this_file_only = not is_library(context)
