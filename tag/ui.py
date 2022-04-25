from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_tags(Menu, ABUOperatorsMenu):
    bl_label = "Tags"

    def setup_ops(self, layout, context):
        self.add_op(layout, "asset.batch_add_tags", "Add", "ADD")
        self.add_op(layout, "asset.batch_remove_tags", "Remove", "REMOVE")
        self.add_op(layout, "asset.tags_add_smart", "Add Smart", "OUTLINER_OB_LIGHT")
