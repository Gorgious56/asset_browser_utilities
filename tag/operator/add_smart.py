from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty

from asset_browser_utilities.core.operator.helper import BatchExecute, BatchFolderOperator
from asset_browser_utilities.tag.smart_tag import SmartTagPG, apply_smart_tag
from asset_browser_utilities.core.helper import copy_simple_property_group


class BatchExecuteOverride(BatchExecute):
    def __init__(self, operator, context):
        smart_tags_cache = SmartTagPG.get_from_cache(context)
        copy_simple_property_group(operator.operator_settings.smart_tag, SmartTagPG.get_from_cache(context))
        self.smart_tags = smart_tags_cache
        super().__init__(operator, context)

    def do_on_asset(self, asset):
        print(self.smart_tags.increment)
        apply_smart_tag(asset, self.smart_tags)


class OperatorProperties(PropertyGroup):
    smart_tag: PointerProperty(type=SmartTagPG)

    def init(self, add=True):
        pass

    def draw(self, layout):
        self.smart_tag.draw(layout)


class ASSET_OT_tags_add_smart(Operator, BatchFolderOperator):
    bl_idname = "asset.tags_add_smart"
    bl_label = "Add Smart Tags"

    operator_settings: PointerProperty(type=OperatorProperties)
    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        self.operator_settings.init(add=True)
        return self._invoke(context, filter_assets=True)
