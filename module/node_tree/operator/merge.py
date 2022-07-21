import bpy
import re

from asset_browser_utilities.module.node_tree.tool import (
    get_all_node_trees_by_type,
    get_all_node_trees_for_an_enum_selector,
)
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, EnumProperty, BoolProperty

from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.module.material.tool import get_all_materials_used_by_assets


class NodeTreeMergeBatchExecute(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        op_props = get_current_operator_properties()
        if op_props.execute_all:
            node_trees_to = [
                bpy.data.node_groups.get(mat_name[0])
                for mat_name in get_all_node_trees_for_an_enum_selector(op_props, None)
            ]
        else:
            node_trees_to = [bpy.data.node_groups.get(op_props.node_tree_name)]
        node_trees_to_name = [m.name for m in node_trees_to]

        if op_props.mode == "Trailing Numbers":
            for node_tree_to in node_trees_to:
                node_trees_from = set()
                for node_tree in get_all_node_trees_by_type(op_props.tree_type):
                    node_tree_name = node_tree.name
                    if node_tree_name in node_trees_to_name:
                        continue
                    search = re.search("\.[0-9]+$", node_tree_name)
                    if search and node_tree_name[0 : search.start()] == node_tree_to.name:
                        node_trees_from.add(node_tree_name)
                    if op_props.tree_type == "SHADER":
                        materials_to_process = set(get_all_materials_used_by_assets(self.assets))
                        for material in materials_to_process:
                            if not material.use_nodes:
                                continue
                            for node in material.node_tree.nodes:
                                if not node.type == "GROUP":
                                    continue
                                if node.node_tree.name in node_trees_from:
                                    node_tree_from = node.node_tree
                                    if len(node_tree_from.nodes) != len(node.node_tree.nodes):
                                        continue
                                    node.node_tree = node_tree_to
                                    Logger.display(
                                        f"{repr(node_tree_from)} replaced by '{repr(node_tree_to)}' in {repr(material)}"
                                    )
                    elif op_props.tree_type == "COMPOSITING":
                        for scene in bpy.data.scenes:
                            if not scene.use_nodes:
                                continue
                            for node in scene.node_tree.nodes:
                                if not node.type == "GROUP":
                                    continue
                                node_tree_from = node.node_tree
                                if len(node_tree_from.nodes) != len(node.node_tree.nodes):
                                    continue
                                node.node_tree = node_tree_to
                                Logger.display(
                                    f"{repr(node_tree_from)} replaced by '{repr(node_tree_to)}' in {repr(scene.node_tree)}"
                                )
                    elif op_props.tree_type == "GEOMETRY":
                        for asset in self.assets:
                            if isinstance(asset, bpy.types.GeometryNodeTree):
                                for node in asset.nodes:
                                    if not node.type == "GROUP":
                                        continue
                                    if node.node_tree.name in node_trees_from:
                                        node_tree_from = node.node_tree
                                        if len(node_tree_from.nodes) != len(node.node_tree.nodes):
                                            continue
                                        node.node_tree = node_tree_to
                                        Logger.display(
                                            f"{repr(node_tree_from)} replaced by '{repr(node_tree_to)}' in {repr(asset)}"
                                        )
                            else:
                                if not hasattr(asset, "modifiers"):
                                    continue
                                for mod in asset.modifiers:
                                    if mod.type != "NODES":
                                        continue
                                    if mod.node_group.name in node_trees_from:
                                        node_tree_from = mod.node_group
                                        if len(node_tree_from.nodes) != len(mod.node_group.nodes):
                                            continue
                                        mod.node_group = node_tree_to
                                        Logger.display(
                                            f"{repr(node_tree_from)} replaced by '{repr(node_tree_to)}' in {repr(mod)}"
                                        )

        self.save_file()
        self.execute_next_blend()


class NodeTreeMergeOperatorProperties(PropertyGroup):
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

    def draw(self, layout):
        box = layout.box()
        box.label(text="Merge Node Trees")
        box.prop(self, "tree_type")
        box.prop(self, "mode")
        box.prop(self, "execute_all")
        if not self.execute_all:
            box.prop(self, "node_tree_name")


class ABU_OT_node_tree_merge(Operator, BatchFolderOperator):
    bl_idname = "abu.node_tree_merge"
    bl_label = "Merge Node Trees"
    bl_description = "Merge node Trees finishing with .001, .002 etc with base material"

    operator_settings: PointerProperty(type=NodeTreeMergeOperatorProperties)
    logic_class = NodeTreeMergeBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=False)
