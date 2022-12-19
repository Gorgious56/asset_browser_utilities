from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.operator.tool import BatchExecute
from asset_browser_utilities.core.operator.tool import BatchFolderOperator


class DescriptionSetBatchExecute(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        description = get_current_operator_properties().description
        for asset in self.assets:
            asset.asset_data.description = description
            Logger.display(f"Set {asset.name}'s description to '{description}'")
        self.save_file()
        self.execute_next_file()


class DescriptionSetOperatorProperties(PropertyGroup):
    description: StringProperty(name="Description")

    def draw(self, layout, context=None):
        layout.prop(self, "description", icon="FILE_TEXT")


class ABU_OT_description_set(Operator, BatchFolderOperator):
    bl_idname = "abu.description_set"
    bl_label = "Batch Set Description"
    bl_description = "Batch Set Description. Leave Field Empty to remove description"

    operator_settings: PointerProperty(type=DescriptionSetOperatorProperties)
    logic_class = DescriptionSetBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
