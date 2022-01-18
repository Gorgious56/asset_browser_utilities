from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.library.execute import BatchExecute
from asset_browser_utilities.library.operator import BatchOperator


class BatchSetAuthor(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        for asset in self.assets:
            asset.asset_data.author = self.author
        self.save_file()
        self.execute_next_blend()


class OperatorProperties(PropertyGroup):
    author: StringProperty(name="Author")

    def draw(self, layout):
        layout.prop(self, "author", icon="USER")


class ASSET_OT_batch_set_author(Operator, ImportHelper, BatchOperator):
    """Batch Set Author Name. Leave Field Empty to remove author"""

    bl_idname = "asset.batch_set_author"
    bl_label = "Batch Set Author"

    operator_settings: PointerProperty(type=OperatorProperties)
    logic_class = BatchSetAuthor

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)