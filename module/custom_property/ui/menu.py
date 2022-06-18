from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_custom_properties(Menu, ABUOperatorsMenu):
    bl_label = "Custom Properties"
    ops_cmd = [
        ("abu.batch_set_custom_property", "Set", "ADD"),
        ("abu.batch_remove_custom_property", "Remove", "REMOVE"),
    ]
