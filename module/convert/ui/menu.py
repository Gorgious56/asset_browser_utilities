from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_convert(Menu, ABUOperatorsMenu):
    bl_label = "Convert"
    ops_cmd = [
        ("abu.model_convert", "Convert Other Formats", "MESH_MONKEY"),
    ]
