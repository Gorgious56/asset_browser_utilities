import bpy
import re


def get_all_node_trees_for_an_enum_selector(self, context):
    mats_enum = get_all_node_trees_for_an_enum_selector.mats_enum
    mats_enum.clear()
    if self.mode == "Trailing Numbers":
        mats_enum = get_all_node_trees_without_trailing_numbers(tree_type=self.tree_type)
        return mats_enum
    else:
        mats_enum = [(material.name,) * 3 for material in bpy.data.materials]
        return mats_enum


get_all_node_trees_for_an_enum_selector.mats_enum = []


def get_all_node_trees_by_type(tree_type):
    return [n_g for n_g in bpy.data.node_groups if n_g.type == tree_type]


def get_all_node_trees_without_trailing_numbers(tree_type):
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
