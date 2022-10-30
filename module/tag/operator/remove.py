from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.filter.name import FilterName
from bpy.types import Operator
from bpy.props import PointerProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.module.tag.operator.tool import TagAddOrRemoveOperatorProperties


class BatchExecuteOverride(BatchExecute):
    def do_on_asset(self, asset):
        super().do_on_asset(asset)
        asset_data = asset.asset_data
        asset_tags = asset_data.tags
        self.execute_tags(asset_tags)

    def execute_tags(self, asset_tags):
        op_props = get_current_operator_properties()
        if op_props.tag_collection.remove_all:
            if op_props.filter_name.active:
                tags_to_remove = [
                    t.name
                    for t in asset_tags
                    if FilterName.filter_static(
                        t.name,
                        op_props.filter_name.method,
                        op_props.filter_name.value,
                        op_props.filter_name.case_sensitive,
                    )
                ]
                self.remove_tags(asset_tags, tags_to_remove)
            else:
                while asset_tags:
                    asset_tags.remove(asset_tags[0])
                Logger.display(f"Removed all tags from {asset_tags.id_data.name}")
        else:
            self.remove_tags(asset_tags, op_props.tags)

    def remove_tags(self, asset_tags, tags_to_remove):
        for i in range(len(asset_tags) - 1, -1, -1):
            if asset_tags[i].name in tags_to_remove:
                asset_tags.remove(asset_tags[i])
        Logger.display(f"Removed tags '{tags_to_remove}' from {asset_tags.id_data.name}")


class ABU_OT_batch_remove_tags(Operator, BatchFolderOperator):
    bl_idname = "abu.batch_remove_tags"
    bl_label = "Remove tags"

    operator_settings: PointerProperty(type=TagAddOrRemoveOperatorProperties)
    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True, init_operator_settings_arguments={"add": False})
