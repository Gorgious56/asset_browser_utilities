from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_tags(Menu, ABUOperatorsMenu):
    bl_label = "Tags"
    ops_cmd = [
        ("abu.batch_add_tags", "Add", "ADD"),
        ("abu.batch_remove_tags", "Remove", "REMOVE"),
        ("abu.tags_add_smart", "Add Smart", "OUTLINER_OB_LIGHT"),
    ]
