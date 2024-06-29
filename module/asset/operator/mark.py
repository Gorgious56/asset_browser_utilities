import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps

from asset_browser_utilities.module.preview.tool import can_preview_be_generated, ensure_diffuse_texture_is_selected
from asset_browser_utilities.module.library.tool import ensure_asset_uuid


class AssetMarkOperatorProperties(PropertyGroup, BaseOperatorProps):
    overwrite: BoolProperty(
        name="Overwrite assets",
        description="Check to re-mark assets and re-generate preview if the item is already an asset",
        default=False,
    )  # type: ignore
    generate_previews: BoolProperty(
        default=True,
        name="Generate Previews",
        description="When marking assets, automatically generate a preview\nUncheck to mark assets really fast",
    )  # type: ignore
    select_diffuse_texture: BoolProperty(
        default=False,
        name="Select Diffuse Texture",
        description="Check this if the generated preview is gray or pink when there should be color",
    )  # type: ignore

    def draw(self, layout, context=None):
        layout.prop(self, "overwrite", icon="ASSET_MANAGER")
        layout.prop(self, "generate_previews", icon="RESTRICT_RENDER_OFF")
        if self.generate_previews:
            layout.prop(self, "select_diffuse_texture", icon="TEXTURE")

    def run_on_asset(self, asset):
        if asset.asset_data and not self.overwrite:
            return False
        asset.asset_mark()
        ensure_asset_uuid(asset)
        if self.generate_previews and can_preview_be_generated(asset):
            if self.select_diffuse_texture:
                ensure_diffuse_texture_is_selected(asset)
            asset.asset_generate_preview()
        Logger.display(f"{bpy.data.filepath}\\{repr(asset)} marked")


class ABU_OT_asset_mark(Operator, BatchFolderOperator):
    bl_idname: str = "abu.asset_mark"
    bl_label: str = "Batch Mark Assets"
    bl_description: str = "Batch Mark Assets"
    INTERVAL_PREVIEW = 0.05

    operator_settings: PointerProperty(type=AssetMarkOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context)
