from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator
from bpy.props import PointerProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.module.tag.operator.tool import TagAddOrRemoveOperatorProperties


class BatchExecuteOverride(BatchExecute):
    def do_on_asset(self, asset):
        super().do_on_asset(asset)
        asset_data = asset.asset_data
        asset_tags = asset_data.tags
        for tag in get_current_operator_properties().tags:
            asset_tags.new(tag, skip_if_exists=True)
            Logger.display(f"Added tag {tag} to {asset.name}")


class ABU_OT_batch_add_tags(Operator, BatchFolderOperator):
    bl_idname = "abu.batch_add_tags"
    bl_label = "Add tags"

    operator_settings: PointerProperty(type=TagAddOrRemoveOperatorProperties)
    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        self.init_operator_settings()
        get_current_operator_properties().init(add=True)
        return self._invoke(context, filter_assets=True)
