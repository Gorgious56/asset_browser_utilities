from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps


class CopyrightSetOperatorProperties(PropertyGroup, BaseOperatorProps):
    copyright: StringProperty(name="Copyright")

    def draw(self, layout, context=None):
        layout.prop(self, "copyright", icon="USER")

    def run_on_asset(self, asset):
        copyright = self.copyright
        asset.asset_data.copyright = copyright
        Logger.display(f"Set {repr(asset)}'s copyright to '{copyright}'")


class ABU_OT_copyright_set(Operator, BatchFolderOperator):
    bl_idname = "abu.copyright_set"
    bl_label = "Batch Set Copyright"
    bl_description = "Batch Set Copyright. Leave Field Empty to remove copyright"

    operator_settings: PointerProperty(type=CopyrightSetOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
