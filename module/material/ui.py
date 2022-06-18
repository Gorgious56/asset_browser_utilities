from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_material(Menu, ABUOperatorsMenu):
    bl_label = "Materials"
    ops_cmd = [
        ("abu.material_merge", "Merge", "AUTOMERGE_ON"),
    ]
