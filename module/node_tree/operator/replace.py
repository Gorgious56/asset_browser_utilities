import bpy

from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, EnumProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps

from asset_browser_utilities.module.node_tree.tool import get_all_node_trees_for_an_enum_selector


class NodeTreeReplaceOperatorProperties(PropertyGroup, BaseOperatorProps):
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

    def draw(self, layout, context=None):
        box = layout.box()
        box.prop(self, "tree_type")
        box.prop(self, "node_tree_old")
        box.prop(self, "node_tree_new")

    def run_in_file(self, attributes=None):
        node_tree_old = bpy.data.node_groups[self.node_tree_old]
        node_tree_new = bpy.data.node_groups[self.node_tree_new]
        node_tree_old.user_remap(node_tree_new)
        Logger.display(f"Replaced {repr(node_tree_old)} with {repr(node_tree_new)}")


class ABU_OT_node_tree_replace(Operator, BatchFolderOperator):
    bl_idname = "abu.node_tree_replace"
    bl_label = "Replace Node Trees"
    bl_description = "Replace node tree A with node tree B"

    operator_settings: PointerProperty(type=NodeTreeReplaceOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=False)
