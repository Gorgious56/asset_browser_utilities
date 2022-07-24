import bpy

from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, EnumProperty

from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator

from asset_browser_utilities.module.node_tree.tool import (
    get_all_node_trees_for_an_enum_selector,
    get_compatible_node_trees,
    replace_node_group_in_node_tree,
)


class NodeTreeReplaceBatchExecute(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        op_props = get_current_operator_properties()
        node_trees_old_names = [op_props.node_tree_old]
        node_tree_new = bpy.data.node_groups[op_props.node_tree_new]

        if op_props.tree_type in ("SHADER", "COMPOSITING", "GEOMETRY"):
            node_trees = get_compatible_node_trees(op_props.tree_type, self.assets)
            for node_tree in node_trees:
                replace_node_group_in_node_tree(node_tree, node_trees_old_names, node_tree_new)
        if op_props.tree_type == "GEOMETRY":
            for asset in self.assets:
                if not isinstance(asset, bpy.types.GeometryNodeTree):
                    if not hasattr(asset, "modifiers"):
                        continue
                    for mod in asset.modifiers:
                        if mod.type != "NODES":
                            continue
                        if mod.node_group.name in node_trees_old_names:
                            old_name = mod.node_group.name
                            mod.node_group = node_tree_new
                            Logger.display(
                                f"'{repr(bpy.data.node_groups[old_name])}' replaced by '{repr(node_tree_new)}' in '{repr(mod)}'"
                            )

        self.save_file()
        self.execute_next_blend()


class NodeTreeReplaceOperatorProperties(PropertyGroup):
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
    node_tree_old: EnumProperty(name="Replace", items=get_all_node_trees_for_an_enum_selector)
    node_tree_new: EnumProperty(name="With", items=get_all_node_trees_for_an_enum_selector)

    def draw(self, layout):
        box = layout.box()
        box.prop(self, "tree_type")
        box.prop(self, "node_tree_old")
        box.prop(self, "node_tree_new")


class ABU_OT_node_tree_replace(Operator, BatchFolderOperator):
    bl_idname = "abu.node_tree_replace"
    bl_label = "Replace Node Trees"
    bl_description = "Replace node tree A with node tree B"

    operator_settings: PointerProperty(type=NodeTreeReplaceOperatorProperties)
    logic_class = NodeTreeReplaceBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=False)
