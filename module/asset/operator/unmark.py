import bpy

from bpy.props import PointerProperty
from bpy.types import Operator, PropertyGroup

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps


class AssetUnmarkOperatorProperties(PropertyGroup, BaseOperatorProps):
    def run_on_asset(self, asset):
        if asset.asset_data:
            asset.asset_clear()
            Logger.display(f"{bpy.data.filepath}\\{repr(asset)} unmarked")
        else:
            return False


class ABU_OT_asset_unmark(Operator, BatchFolderOperator):
    bl_idname = "abu.asset_unmark"
    bl_label = "Batch Unmark Assets"
    bl_options = {"UNDO"}

    operator_settings: PointerProperty(type=AssetUnmarkOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
