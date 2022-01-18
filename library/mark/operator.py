from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
from bpy.props import PointerProperty

from asset_browser_utilities.library.operator import BatchOperator
from .helper import BatchMark, BatchUnmark
from .prop import OperatorProperties as MarkOrUnmarkOperatorProperties


class ASSET_OT_batch_mark(Operator, ImportHelper, BatchOperator):
    "Batch Mark Assets"
    bl_idname = "asset.batch_mark"
    bl_label = "Batch Mark Assets"

    operator_settings: PointerProperty(type=MarkOrUnmarkOperatorProperties)
    logic_class = BatchMark

    def invoke(self, context, event):
        self.operator_settings.mark = True
        return self._invoke(context)


class ASSET_OT_batch_unmark(Operator, ImportHelper, BatchOperator):
    "Batch Unmark Assets"
    bl_idname = "asset.batch_unmark"
    bl_label = "Batch Unmark Assets"

    operator_settings: PointerProperty(type=MarkOrUnmarkOperatorProperties)
    logic_class = BatchUnmark

    def invoke(self, context, event):
        self.operator_settings.mark = False
        return self._invoke(context)
