from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_custom_properties(Menu, ABUOperatorsMenu):
    bl_label = "Custom Properties"

    def setup_ops(self, layout, context):
        self.add_op(layout, "abu.batch_set_custom_property", "Set", "ADD")
        self.add_op(layout, "abu.batch_remove_custom_property", "Remove", "REMOVE")
