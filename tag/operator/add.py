from bpy.types import Operator
from bpy.props import PointerProperty

from asset_browser_utilities.core.operator.helper import BatchExecute, BatchFolderOperator
from asset_browser_utilities.tag.operator.tool import AddOrRemoveTagsOperatorProperties


class BatchExecuteOverride(BatchExecute):
    def __init__(self, operator, context):
        self.tags = [t.name for t in operator.operator_settings.tag_collection.items if not t.is_empty()]
        super().__init__(operator, context)

    def do_on_asset(self, asset):
        asset_data = asset.asset_data
        asset_tags = asset_data.tags
        for tag in self.tags:
            asset_tags.new(tag, skip_if_exists=True)


class ASSET_OT_batch_add_tags(Operator, BatchFolderOperator):
    "Add tags"
    bl_idname = "asset.batch_add_tags"
    bl_label = "Add tags"

    operator_settings: PointerProperty(type=AddOrRemoveTagsOperatorProperties)
    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        self.operator_settings.init(add=True)
        return self._invoke(context, filter_assets=True)
