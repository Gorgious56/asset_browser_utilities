from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_custom_properties(Menu, ABUOperatorsMenu):
    bl_label = "Custom Properties"
    ops_cmd = [
        ("abu.custom_property_set", "Set", "ADD"),
        ("abu.custom_property_remove", "Remove", "REMOVE"),
    ]
