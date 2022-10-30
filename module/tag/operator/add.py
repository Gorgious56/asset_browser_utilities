from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator
from bpy.props import PointerProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.module.tag.operator.tool import TagAddOrRemoveOperatorProperties


class TagAddBatchExecute(BatchExecute):
    def do_on_asset(self, asset):
        super().do_on_asset(asset)
        asset_data = asset.asset_data
        asset_tags = asset_data.tags
        for tag in get_current_operator_properties().tags:
            asset_tags.new(tag, skip_if_exists=True)
            Logger.display(f"Added tag '{tag}' to {asset.name}")


class ABU_OT_tag_add(Operator, BatchFolderOperator):
    bl_idname = "abu.tag_add"
    bl_label = "Add tags"

    operator_settings: PointerProperty(type=TagAddOrRemoveOperatorProperties)
    logic_class = TagAddBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True, init_operator_settings_arguments={"add": True})
