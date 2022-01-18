import bpy.app.timers
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.library.execute import BatchExecute
from asset_browser_utilities.library.operator import BatchOperator
from asset_browser_utilities.preview.helper import is_preview_generated


class BatchGeneratePreviews(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        for asset in self.assets:
            if self.overwrite or not is_preview_generated(asset):
                asset.asset_generate_preview()

        bpy.app.timers.register(self.sleep_until_previews_are_done_and_execute_next_file)


class OperatorProperties(PropertyGroup):
    overwrite: BoolProperty(
        name="Overwrite Previews",
        description="Check to re-generate previews of assets that already have one",
        default=False,
    )

    def draw(self, layout):
        layout.prop(self, "overwrite", icon="ASSET_MANAGER")


class ASSET_OT_batch_generate_previews(Operator, ImportHelper, BatchOperator):
    "Batch Generate Previews"
    bl_idname = "asset.batch_generate_previews"
    bl_label = "Batch Generate Previews"

    operator_settings: PointerProperty(type=OperatorProperties)
    logic_class = BatchGeneratePreviews

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
