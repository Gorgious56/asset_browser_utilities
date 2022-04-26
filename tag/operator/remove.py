from bpy.types import Operator
from bpy.props import PointerProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.tag.operator.tool import AddOrRemoveTagsOperatorProperties


class BatchExecuteOverride(BatchExecute):
    def __init__(self, operator, context):
        self.tags = [t.name for t in operator.operator_settings.tag_collection.items if not t.is_empty()]
        self.remove_all = operator.operator_settings.tag_collection.remove_all
        super().__init__(operator, context)

    def do_on_asset(self, asset):
        super().do_on_asset(asset)
        asset_data = asset.asset_data
        asset_tags = asset_data.tags
        self.execute_tags(asset_tags)

    def execute_tags(self, asset_tags):
        if self.remove_all:
            while asset_tags:
                asset_tags.remove(asset_tags[0])
        else:
            self.remove_tags(asset_tags, self.tags)

    def remove_tags(self, asset_tags, tags_to_remove):
        for i in range(len(asset_tags) - 1, -1, -1):
            if asset_tags[i].name in tags_to_remove:
                asset_tags.remove(asset_tags[i])



class ASSET_OT_batch_remove_tags(Operator, BatchFolderOperator):
    "Remove tags"
    bl_idname = "asset.batch_remove_tags"
    bl_label = "Remove tags"

    operator_settings: PointerProperty(type=AddOrRemoveTagsOperatorProperties)
    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        self.operator_settings.init(add=False)
        return self._invoke(context, filter_assets=True)
