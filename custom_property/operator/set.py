from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty, FloatProperty, IntProperty, FloatVectorProperty, EnumProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator


class BatchExecuteOverride(BatchExecute):
    def do_on_asset(self, asset):
        op_props = get_current_operator_properties()
        prop_name = op_props.name
        prop_value = op_props.value
        asset_data = asset.asset_data
        asset_data[prop_name] = prop_value
        if isinstance(prop_value, list):  # Color
            asset_data.id_properties_ensure()
            property_manager = asset_data.id_properties_ui(prop_name)
            property_manager.update(subtype="COLOR")
        Logger.display(f"Added custom property '{prop_name=}', '{prop_value=}' to {asset.name}")
        super().do_on_asset(asset)


class CustomPropertySetOperatorProperties(PropertyGroup):
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
    
    @property
    def value(self):
        if self.type == "value_color":
            return [c for c in getattr(self, self.type)]
        else:
            return getattr(self, self.type)

    def draw(self, layout):
        box = layout.box()
        box.prop(self, "name")
        box.prop(self, "type")
        box.prop(self, self.type, text="Value")


class ABU_OT_batch_set_custom_property(Operator, BatchFolderOperator):
    bl_idname = "abu.batch_set_custom_property"
    bl_label = "Set Custom Property"

    operator_settings: PointerProperty(type=CustomPropertySetOperatorProperties)
    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
