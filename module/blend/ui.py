from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_blend(Menu, ABUOperatorsMenu):
    bl_label = "Blend"
    ops_cmd = [
        ("abu.blend_rename", "Rename", "FILE_TEXT"),
    ]
