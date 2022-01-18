from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.helper import is_library


class ABU_MT_assets(Menu):
    bl_label = "Assets"

    def draw(self, context):
        layout = self.layout
        this_file_only = not is_library(context)
        mark_op = layout.operator("asset.batch_mark", text="Mark", icon="SHADERFX")
        mark_op.library_settings.this_file_only = this_file_only
        unmark_op = layout.operator("asset.batch_unmark", text="Unmark", icon="TRASH")
        unmark_op.library_settings.this_file_only = this_file_only
