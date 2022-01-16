from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

from asset_browser_utilities.library.operator import BatchOperator
from .helper import BatchGeneratePreviews


class ASSET_OT_batch_generate_previews(Operator, ImportHelper, BatchOperator):
    bl_idname = "asset.batch_generate_previews"
    bl_label = "Batch Generate Previews"

    logic_class = BatchGeneratePreviews

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
