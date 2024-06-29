from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps

from asset_browser_utilities.module.preview.tool import can_preview_be_generated, ensure_diffuse_texture_is_selected


class PreviewGenerateOperatorProperties(PropertyGroup, BaseOperatorProps):
    overwrite: BoolProperty(
        name="Overwrite Previews",
        description="Check to re-generate previews of assets that already have one",
        default=False,
    )  # type: ignore
    select_diffuse_texture: BoolProperty(
        default=False,
        name="Select Diffuse Texture",
        description="Check this if the generated preview is gray or pink when there should be color",
    )  # type: ignore

    def draw(self, layout, context=None):
        layout.prop(self, "overwrite", icon="ASSET_MANAGER")
        layout.prop(self, "select_diffuse_texture", icon="TEXTURE")

    def run_on_asset(self, asset, attributes=None):
        if (self.overwrite or not asset.preview) and can_preview_be_generated(asset):
            if self.select_diffuse_texture:
                ensure_diffuse_texture_is_selected(asset)
            asset.asset_generate_preview()
            Logger.display(f"Launched preview generation for {asset.name}")
        else:
            return False


class ABU_OT_preview_generate(Operator, BatchFolderOperator):
    bl_idname = "abu.preview_generate"
    bl_label = "Batch Generate Previews"

    operator_settings: PointerProperty(type=PreviewGenerateOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
