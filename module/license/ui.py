from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_license(Menu, ABUOperatorsMenu):
    bl_label = "License"
    ops_cmd = [
        ("abu.license_set", "Set", "ADD"),
    ]
