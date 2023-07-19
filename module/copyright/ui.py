from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_copyright(Menu, ABUOperatorsMenu):
    bl_label = "Copyright"
    ops_cmd = [
        ("abu.copyright_set", "Set", "ADD"),
    ]
