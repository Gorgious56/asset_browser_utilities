from bpy.types import Operator
from bpy.props import PointerProperty

from asset_browser_utilities.core.operator.tool import BatchFolderOperator

from asset_browser_utilities.module.tag.tool import TagAddOrRemoveOperatorProperties


class ABU_OT_tag_add(Operator, BatchFolderOperator):
    bl_idname = "abu.tag_add"
    bl_label = "Add tags"

    operator_settings: PointerProperty(type=TagAddOrRemoveOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True, init_operator_settings_arguments={"add": True})
