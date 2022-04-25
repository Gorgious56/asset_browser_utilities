from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_description(Menu, ABUOperatorsMenu):
    bl_label = "Description"

    def setup_ops(self, layout, context):
        self.add_op(layout, "asset.batch_set_description", "Set", "ADD")
