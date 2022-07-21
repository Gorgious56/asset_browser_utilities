import re
from asset_browser_utilities.module.material.tool import get_all_materials_used_by_assets
import bpy
from asset_browser_utilities.core.log.logger import Logger


def get_all_node_trees_for_an_enum_selector(self, context):
    node_trees_enum = get_all_node_trees_for_an_enum_selector.mats_enum
    node_trees_enum.clear()
    if hasattr(self, "mode") and self.mode == "Trailing Numbers":
        return get_all_node_trees_by_type_without_trailing_numbers_for_an_enum_selector(tree_type=self.tree_type)
    else:
        return [(n_g.name,) * 3 for n_g in get_all_node_trees_by_type(tree_type=self.tree_type)]


get_all_node_trees_for_an_enum_selector.mats_enum = []


def get_all_node_trees_by_type(tree_type):
    return [n_g for n_g in bpy.data.node_groups if n_g.type == tree_type]


def get_all_node_trees_by_type_without_trailing_numbers_for_an_enum_selector(tree_type):
    all_node_trees = set(m.name for m in get_all_node_trees_by_type(tree_type))
    duplicate_trees = set()
    for tree_name in all_node_trees:
        search = re.search("\.[0-9]+$", tree_name)
        if search:
            base_name = tree_name[0 : search.start()]
            if base_name in all_node_trees:
                duplicate_trees.add(tree_name[0 : search.start()])
    duplicate_trees.discard("Geometry Nodes")  # We don't want to overwrite plain old node trees. Rename them !
    duplicate_trees = sorted(list(duplicate_trees))
    return [(m,) * 3 for m in duplicate_trees]


def replace_node_group_in_node_tree(node_tree, group_names_old, group_new):
    for node in node_tree.nodes:
        if not node.type == "GROUP":
            continue
        if node.node_tree.name in group_names_old:
            old_name = node.node_tree.name
            node.node_tree = group_new
            Logger.display(
                f"'{repr(bpy.data.node_groups[old_name])}' replaced by '{repr(group_new)}' in {repr(node_tree)}"
            )


def get_compatible_node_trees(tree_type, assets):
    if tree_type == "SHADER":
        for material in set(get_all_materials_used_by_assets(assets)):
            if not material.use_nodes:
                continue
            yield material.node_tree
    elif tree_type == "COMPOSITING":
        for scene in bpy.data.scenes:
            if not scene.use_nodes:
                continue
            yield scene.node_tree
    elif tree_type == "GEOMETRY":
        for asset in assets:
            if isinstance(asset, bpy.types.GeometryNodeTree):
                yield asset
