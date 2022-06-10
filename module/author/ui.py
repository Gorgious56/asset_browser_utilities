from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_author(Menu, ABUOperatorsMenu):
    bl_label = "Author"

    def setup_ops(self, layout, context):
        self.add_op(layout, "abu.author_set", "Set", "ADD")
