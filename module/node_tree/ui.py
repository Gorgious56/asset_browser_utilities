from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_node_tree(Menu, ABUOperatorsMenu):
    bl_label = "Node Trees"
    ops_cmd = [
        ("abu.node_tree_merge", "Merge", "AUTOMERGE_ON"),
    ]
