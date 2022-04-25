
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty, FloatProperty, IntProperty, FloatVectorProperty, EnumProperty

from asset_browser_utilities.core.operator.helper import BatchExecute, BatchFolderOperator


class BatchExecuteOverride(BatchExecute):
    def __init__(self, operator, context):
        self.custom_prop_name = operator.operator_settings.name
        if operator.operator_settings.type == "value_color":
            self.custom_prop_value = [c for c in getattr(operator.operator_settings, operator.operator_settings.type)]
        else:
            self.custom_prop_value = getattr(operator.operator_settings, operator.operator_settings.type)
        super().__init__(operator, context)

    def do_on_asset(self, asset):
        super().do_on_asset(asset)
        asset_data = asset.asset_data
        asset_data[self.custom_prop_name] = self.custom_prop_value


class SetCustomPropertyOperatorProperties(PropertyGroup):
    name: StringProperty(name="Name", default="prop")
    type: EnumProperty(
        name="Type",
        items=(
            ("value_str", "String", ""),
            ("value_int", "Integer", ""),
            ("value_float", "Float", ""),
            ("value_color", "Color", ""),
        ),
    )
    value_str: StringProperty()
    value_float: FloatProperty()
    value_int: IntProperty()
    value_color: FloatVectorProperty(subtype="COLOR", min=0, max=1, default=(1, 1, 1, 1), size=4)

    def draw(self, layout):
        box = layout.box()
        box.prop(self, "name")
        box.prop(self, "type")
        box.prop(self, self.type, text="Value")


class ASSET_OT_batch_set_custom_property(Operator, BatchFolderOperator):
    bl_idname = "asset.batch_set_custom_property"
    bl_label = "Set Custom Property"

    operator_settings: PointerProperty(type=SetCustomPropertyOperatorProperties)
    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
