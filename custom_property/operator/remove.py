
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty, FloatProperty, IntProperty, FloatVectorProperty, EnumProperty

from asset_browser_utilities.core.operator.helper import BatchExecute, BatchFolderOperator


class BatchExecuteOverride(BatchExecute):
    def __init__(self, operator, context):
        self.custom_prop_name = operator.operator_settings.name
        super().__init__(operator, context)

    def do_on_asset(self, asset):
        super().do_on_asset(asset)
        asset_data = asset.asset_data
        try:
            del asset_data[self.custom_prop_name]
        except KeyError:
            pass


class RemoveCustomPropertyOperatorProperties(PropertyGroup):
    name: StringProperty(name="Name", default="prop")

    def draw(self, layout):
        layout.prop(self, "name", text="Custom Property Name")


class ASSET_OT_batch_remove_custom_property(Operator, BatchFolderOperator):
    bl_idname = "asset.batch_remove_custom_property"
    bl_label = "Remove Custom Property"

    operator_settings: PointerProperty(type=RemoveCustomPropertyOperatorProperties)
    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
