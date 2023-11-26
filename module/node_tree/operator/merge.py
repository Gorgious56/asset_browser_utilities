import re

import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, EnumProperty, BoolProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps

from asset_browser_utilities.module.node_tree.tool import (
    get_all_node_trees_by_type,
    get_all_node_trees_for_an_enum_selector,
)


class NodeTreeMergeOperatorProperties(PropertyGroup, BaseOperatorProps):
    mode: EnumProperty(
        name="Mode", items=(("Trailing Numbers", "Trailing Numbers", "Trailing Numbers", "LINENUMBERS_ON", 0),)
    )
    tree_type: EnumProperty(
        name="Type",
        items=(
            ("SHADER", "Shader", "", "NODE_MATERIAL", 1),
            # ("TEXTURE", "Texture", "", "TEXTURE", 2),
            ("COMPOSITING", "Compositing", "", "NODE_COMPOSITING", 4),
            ("GEOMETRY", "Geometry Nodes", "", "OUTLINER_DATA_MESH", 8),
        ),
        default="SHADER",
    )
    execute_all: BoolProperty(name="Merge all duplicate node trees", default=False)
    node_tree_name: EnumProperty(name="Base Node Tree", items=get_all_node_trees_for_an_enum_selector)

    def draw(self, layout, context=None):
        box = layout.box()
        box.label(text="Merge Node Trees")
        box.prop(self, "tree_type")
        box.prop(self, "mode")
        box.prop(self, "execute_all")
        if not self.execute_all:
            box.prop(self, "node_tree_name")

    def run_in_file(self, attributes=None):
        if self.execute_all:
            node_trees_to_keep = [
                bpy.data.node_groups.get(mat_name[0])
                for mat_name in get_all_node_trees_for_an_enum_selector(self, None)
            ]
        else:
            node_trees_to_keep = [bpy.data.node_groups.get(self.node_tree_name)]
        node_trees_to_name = [m.name for m in node_trees_to_keep]

        if self.mode == "Trailing Numbers":
            for node_tree_to_keep in node_trees_to_keep:
                node_trees_to_override = set()
                for node_tree in get_all_node_trees_by_type(self.tree_type):
                    node_tree_name = node_tree.name
                    if node_tree_name in node_trees_to_name:
                        continue
                    search = re.search("\.[0-9]+$", node_tree_name)
                    if search and node_tree_name[0 : search.start()] == node_tree_to_keep.name:
                        node_trees_to_override.add(node_tree)
                for node_tree_to_override in node_trees_to_override:
                    node_tree_to_override.user_remap(node_tree_to_keep)
                    Logger.display(f"Replaced {repr(node_tree_to_override)} with {repr(node_tree_to_keep)}")


class ABU_OT_node_tree_merge(Operator, BatchFolderOperator):
    bl_idname = "abu.node_tree_merge"
    bl_label = "Merge Node Trees"
    bl_description = "Merge node Trees finishing with .001, .002 etc with base material"

    operator_settings: PointerProperty(type=NodeTreeMergeOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=False)
