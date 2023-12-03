from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, EnumProperty, StringProperty, IntProperty, BoolProperty

from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps

from asset_browser_utilities.module.tag.smart_tag import SmartTag, apply_smart_tag


class TagAddSmartOperatorProperties(PropertyGroup, BaseOperatorProps):
    operation: EnumProperty(name="Operation", items=[(s_t.value,) * 3 for s_t in SmartTag])
    custom_property_name: StringProperty(name="Custom Property Name")
    increment: IntProperty(min=1, default=500, name="Increment")
    round_mode: EnumProperty(name="Round", items=(("Up",) * 3, ("Down",) * 3))
    overwrite: BoolProperty(name="Overwrite")

    def draw(self, layout, context=None):
        box = layout.box()
        box.label(text="Smart Tag")
        box.prop(self, "operation", text="")
        if self.operation == SmartTag.CustomProperty.value:
            box.prop(self, "custom_property_name")
        if self.operation in (SmartTag.TriangleCount.value, SmartTag.VertexCount.value):
            box.prop(self, "increment")
            box.prop(self, "round_mode")
        box.prop(self, "overwrite", toggle=True)

    def run_on_asset(self, asset):
        return apply_smart_tag(asset, self)


class ABU_OT_tag_add_smart(Operator, BatchFolderOperator):
    bl_idname = "abu.tag_add_smart"
    bl_label = "Add Smart Tags"

    operator_settings: PointerProperty(type=TagAddSmartOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
