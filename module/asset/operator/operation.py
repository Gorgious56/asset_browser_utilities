import bpy
from bpy.types import Operator

from asset_browser_utilities.core.operator.tool import BatchFolderOperator


class ASSET_OT_batch_operate(Operator, BatchFolderOperator):
    bl_idname = "asset.batch_operate"
    bl_label = "Batch Operate On Assets"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return self._invoke(context)
