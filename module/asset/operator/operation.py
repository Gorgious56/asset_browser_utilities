import bpy
from bpy.types import Operator

from asset_browser_utilities.core.operator.tool import BatchFolderOperator


class ABU_OT_batch_operate(Operator, BatchFolderOperator):
    bl_idname = "abu.batch_operate"
    bl_label = "Batch Operate On Assets"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return self._invoke(context)
