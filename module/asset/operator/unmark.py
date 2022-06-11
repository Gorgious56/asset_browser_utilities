from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator


class AssetUnmarkBatchExecute(BatchExecute):
    def do_on_asset(self, asset):
        super().do_on_asset(asset)
        if asset.asset_data:
            asset.asset_clear()
            Logger.display(f"{repr(asset)} Unmarked")


class ASSET_OT_batch_unmark(Operator, BatchFolderOperator):
    bl_idname = "asset.batch_unmark"
    bl_label = "Batch Unmark Assets"
    bl_options = {"UNDO"}

    logic_class = AssetUnmarkBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
