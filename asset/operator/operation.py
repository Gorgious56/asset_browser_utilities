import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator


class BatchExecuteOverride(BatchExecute):
    pass


class OperatorProperties(PropertyGroup):
    pass


class ASSET_OT_batch_operate(Operator, BatchFolderOperator):
    bl_idname = "asset.batch_operate"
    bl_label = "Batch Operate On Assets"
    bl_options = {"REGISTER", "UNDO"}

    operator_settings: PointerProperty(type=OperatorProperties)
    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        return self._invoke(context)
