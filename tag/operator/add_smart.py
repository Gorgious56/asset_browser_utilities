from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, EnumProperty, StringProperty, IntProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.tag.smart_tag import SmartTag, apply_smart_tag


class BatchExecuteOverride(BatchExecute):
    def do_on_asset(self, asset):
        apply_smart_tag(asset, get_current_operator_properties())
        super().do_on_asset(asset)


class OperatorProperties(PropertyGroup):
    operation: EnumProperty(name="Operation", items=[(s_t.value,) * 3 for s_t in SmartTag])
    custom_property_name: StringProperty(name="Custom Property Name")
    increment: IntProperty(min=1, default=500, name="Increment")
    round_mode: EnumProperty(name="Round", items=(("Up",) * 3, ("Down",) * 3))

    def draw(self, layout, context=None):
        box = layout.box()
        box.label(text="Smart Tag")
        box.prop(self, "operation", text="")
        if self.operation == SmartTag.CustomProperty.value:
            box.prop(self, "custom_property_name")
        if self.operation in (SmartTag.TriangleCount.value, SmartTag.VertexCount.value):
            box.prop(self, "increment")
            box.prop(self, "round_mode")


class ABU_OT_tags_add_smart(Operator, BatchFolderOperator):
    bl_idname = "abu.tags_add_smart"
    bl_label = "Add Smart Tags"

    operator_settings: PointerProperty(type=OperatorProperties)
    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
