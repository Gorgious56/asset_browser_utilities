from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProperties
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.file.path import get_current_file_path


class AuthorSetOperatorProperties(PropertyGroup, BaseOperatorProperties):
    author: StringProperty(name="Author")

    def draw(self, layout, context=None):
        layout.prop(self, "author", icon="USER")

    def do_on_asset(self, asset):
        asset.asset_data.author = self.author
        Logger.display(f"{get_current_file_path()} : Set {repr(asset)}'s author to '{self.author}'")


class ABU_OT_author_set(Operator, BatchFolderOperator):
    bl_idname = "abu.author_set"
    bl_label = "Batch Set Author"
    bl_description = "Batch Set Author Name. Leave Field Empty to remove author"

    operator_settings: PointerProperty(type=AuthorSetOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
