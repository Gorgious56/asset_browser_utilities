from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps


class LicenseSetOperatorProperties(PropertyGroup, BaseOperatorProps):
    license: StringProperty(name="License")

    def draw(self, layout, context=None):
        layout.prop(self, "license", icon="USER")

    def run_on_asset(self, asset):
        for asset in self.assets:
            asset.asset_data.license = self.license
            Logger.display(f"Set {repr(asset)}'s license to '{self.license}'")


class ABU_OT_license_set(Operator, BatchFolderOperator):
    bl_idname = "abu.license_set"
    bl_label = "Batch Set License"
    bl_description = "Batch Set License. Leave Field Empty to remove license"

    operator_settings: PointerProperty(type=LicenseSetOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
