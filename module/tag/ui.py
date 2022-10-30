from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_tags(Menu, ABUOperatorsMenu):
    bl_label = "Tags"
    ops_cmd = [
        ("abu.tag_add", "Add", "ADD"),
        ("abu.tag_remove", "Remove", "REMOVE"),
        ("abu.tag_add_smart", "Add Smart", "OUTLINER_OB_LIGHT"),
    ]
