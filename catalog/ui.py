from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.helper import is_library


class ABU_MT_catalogs(Menu):
    bl_label = "Catalogs"

    def draw(self, context):
        layout = self.layout
        this_file_only = not is_library(context)
        mark_op = layout.operator("asset.batch_move_to_catalog", text="Move To Catalog", icon="ADD")
        mark_op.library_settings.this_file_only = this_file_only
        mark_op = layout.operator("asset.batch_remove_from_catalog", text="Remove From Catalog", icon="REMOVE")
        mark_op.library_settings.this_file_only = this_file_only
