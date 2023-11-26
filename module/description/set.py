from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps


class DescriptionSetOperatorProperties(PropertyGroup, BaseOperatorProps):
    description: StringProperty(name="Description")

    def draw(self, layout, context=None):
        layout.prop(self, "description", icon="FILE_TEXT")

    def run_on_asset(self, asset):
        description = self.description
        asset.asset_data.description = description
        Logger.display(f"Set {asset.name}'s description to '{description}'")


class ABU_OT_description_set(Operator, BatchFolderOperator):
    bl_idname = "abu.description_set"
    bl_label = "Batch Set Description"
    bl_description = "Batch Set Description. Leave Field Empty to remove description"

    operator_settings: PointerProperty(type=DescriptionSetOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
