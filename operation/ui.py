from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_operations(Menu, ABUOperatorsMenu):
    bl_label = "Operations"

    def setup_ops(self, layout, context):
        self.add_op(layout, "asset.batch_operate", "Custom Operation", "MODIFIER")
