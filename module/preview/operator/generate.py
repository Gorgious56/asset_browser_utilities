from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps


class PreviewGenerateOperatorProperties(PropertyGroup, BaseOperatorProps):
    overwrite: BoolProperty(
        name="Overwrite Previews",
        description="Check to re-generate previews of assets that already have one",
        default=False,
    )
    generate_previews: BoolProperty(default=True)

    def draw(self, layout, context=None):
        layout.prop(self, "overwrite", icon="ASSET_MANAGER")

    def run_on_asset(self, asset):
        if self.overwrite or not asset.preview:
            asset.asset_generate_preview()
            Logger.display(f"Launched preview generation for {asset.name}")


class ABU_OT_preview_generate(Operator, BatchFolderOperator):
    bl_idname = "abu.preview_generate"
    bl_label = "Batch Generate Previews"

    operator_settings: PointerProperty(type=PreviewGenerateOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
