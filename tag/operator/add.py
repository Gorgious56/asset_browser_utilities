import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty

from asset_browser_utilities.core.operator.helper import BatchExecute, BatchFolderOperator
from asset_browser_utilities.tag.tag_collection import TagCollection


class BatchExecuteOverride(BatchExecute):
    def __init__(self, operator, context):
        self.tags = [t.name for t in operator.operator_settings.tag_collection.items if not t.is_empty()]
        super().__init__(operator, context)

    def do_on_asset(self, asset):
        asset_data = asset.asset_data
        asset_tags = asset_data.tags
        self.execute_tags(asset_tags)

    def execute_tags(self, asset_tags):
        existing_tags = [tag.name for tag in asset_tags]
        for tag in self.tags:
            if tag in existing_tags:
                continue
            asset_tags.new(tag)


class OperatorProperties(PropertyGroup):
    tag_collection: PointerProperty(type=TagCollection)
    MAX_TAGS = 10

    def init(self, add=True):
        self.tag_collection.add = add
        self.tag_collection.init(tags=self.MAX_TAGS)

    def draw(self, layout):
        self.tag_collection.draw(layout)


class ASSET_OT_batch_add_tags(Operator, BatchFolderOperator):
    "Add tags"
    bl_idname = "asset.batch_add_tags"
    bl_label = "Add tags"

    operator_settings: PointerProperty(type=OperatorProperties)
    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        self.operator_settings.init(add=True)
        return self._invoke(context, filter_assets=True)
