from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.library.execute import BatchExecute
from asset_browser_utilities.library.operator import BatchOperator


class BatchAddDescription(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        for asset in self.assets:
            asset.asset_data.description = self.description
        self.save_file()
        self.execute_next_blend()


class OperatorProperties(PropertyGroup):
    description: StringProperty(name="Description")

    def draw(self, layout):
        layout.prop(self, "description", icon="FILE_TEXT")


class ASSET_OT_batch_add_description(Operator, ImportHelper, BatchOperator):
    """Batch Set Description. Leave Field Empty to remove description"""

    bl_idname = "asset.batch_add_description"
    bl_label = "Batch Add Description"

    operator_settings: PointerProperty(type=OperatorProperties)
    logic_class = BatchAddDescription

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
