from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps


class CustomPropertyRemoveOperatorProperties(PropertyGroup, BaseOperatorProps):
    name: StringProperty(name="Name", default="prop")

    def draw(self, layout, context=None):
        layout.prop(self, "name", text="Custom Property Name")

    def run_on_asset(self, asset):
        prop_name = get_current_operator_properties().name
        asset_data = asset.asset_data
        try:
            del asset_data[prop_name]
        except KeyError:
            pass
        else:
            Logger.display(f"Removed custom property '{prop_name}' from '{asset.name}'")
        super().run_on_asset(asset)


class ABU_OT_custom_property_remove(Operator, BatchFolderOperator):
    bl_idname = "abu.custom_property_remove"
    bl_label = "Remove Custom Property"

    operator_settings: PointerProperty(type=CustomPropertyRemoveOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
