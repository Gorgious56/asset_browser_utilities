from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator


class AuthorSetBatchExecute(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        author = get_current_operator_properties().author
        for asset in self.assets:
            asset.asset_data.author = author
            Logger.display(f"Set {repr(asset)}'s author to '{author}'")
        self.save_file()
        self.execute_next_blend()


class AuthorSetOperatorProperties(PropertyGroup):
    author: StringProperty(name="Author")

    def draw(self, layout, context=None):
        layout.prop(self, "author", icon="USER")


class ABU_OT_author_set(Operator, BatchFolderOperator):
    bl_idname = "abu.author_set"
    bl_label = "Batch Set Author"
    bl_description = "Batch Set Author Name. Leave Field Empty to remove author"

    operator_settings: PointerProperty(type=AuthorSetOperatorProperties)
    logic_class = AuthorSetBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
