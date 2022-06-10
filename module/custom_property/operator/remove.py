
from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty, FloatProperty, IntProperty, FloatVectorProperty, EnumProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator


class BatchExecuteOverride(BatchExecute):
    def do_on_asset(self, asset):
        prop_name = get_current_operator_properties().name
        asset_data = asset.asset_data
        try:
            del asset_data[prop_name]
        except KeyError:
            pass
        else:
            Logger.display(f"Removed custom property '{prop_name}' from '{asset.name}'")
        super().do_on_asset(asset)


class RemoveCustomPropertyOperatorProperties(PropertyGroup):
    name: StringProperty(name="Name", default="prop")

    def draw(self, layout):
        layout.prop(self, "name", text="Custom Property Name")


class ABU_OT_batch_remove_custom_property(Operator, BatchFolderOperator):
    bl_idname = "abu.batch_remove_custom_property"
    bl_label = "Remove Custom Property"

    operator_settings: PointerProperty(type=RemoveCustomPropertyOperatorProperties)
    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
