from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator


class LicenseSetBatchExecute(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        license = get_current_operator_properties().license
        for asset in self.assets:
            asset.asset_data.license = license
            Logger.display(f"Set {repr(asset)}'s license to '{license}'")
        self.save_file()
        self.execute_next_file()


class LicenseSetOperatorProperties(PropertyGroup):
    license: StringProperty(name="License")

    def draw(self, layout, context=None):
        layout.prop(self, "license", icon="USER")


class ABU_OT_license_set(Operator, BatchFolderOperator):
    bl_idname = "abu.license_set"
    bl_label = "Batch Set License"
    bl_description = "Batch Set License. Leave Field Empty to remove license"

    operator_settings: PointerProperty(type=LicenseSetOperatorProperties)
    logic_class = LicenseSetBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
