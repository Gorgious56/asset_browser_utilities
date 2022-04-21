from bpy.types import Operator

from asset_browser_utilities.core.operator.helper import BatchExecute, BatchFolderOperator


class BatchExecuteOverride(BatchExecute):
    def do_on_asset(self, asset):
        asset.asset_clear()

class ASSET_OT_batch_unmark(Operator, BatchFolderOperator):
    "Batch Unmark Assets"
    bl_idname = "asset.batch_unmark"
    bl_label = "Batch Unmark Assets"
    bl_options = {"UNDO"}

    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
