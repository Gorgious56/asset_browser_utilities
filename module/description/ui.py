from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_description(Menu, ABUOperatorsMenu):
    bl_label = "Description"
    ops_cmd = [
        ("abu.description_set", "Set", "ADD"),
    ]
