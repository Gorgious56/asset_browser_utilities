from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_catalogs(Menu, ABUOperatorsMenu):
    bl_label = "Catalogs"

    def setup_ops(self, layout, context):
        self.add_op(layout, "asset.batch_move_to_catalog", "Move To Catalog", "ADD")
        self.add_op(layout, "asset.batch_remove_from_catalog", "Remove From Catalog", "REMOVE")
        self.add_op(layout, "asset.batch_move_from_cat_a_to_cat_b", "Move From A to B", "FOLDER_REDIRECT")
