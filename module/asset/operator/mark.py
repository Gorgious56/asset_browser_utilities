import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProperties

from asset_browser_utilities.module.preview.tool import can_preview_be_generated
from asset_browser_utilities.module.library.tool import ensure_asset_uuid


class AssetMarkOperatorProperties(PropertyGroup, BaseOperatorProperties):
    overwrite: BoolProperty(
        name="Overwrite assets",
        description="Check to re-mark assets and re-generate preview if the item is already an asset",
        default=False,
    )
    generate_previews: BoolProperty(
        default=True,
        name="Generate Previews",
        description="When marking assets, automatically generate a preview\nUncheck to mark assets really fast",
    )

    def draw(self, layout, context=None):
        layout.prop(self, "overwrite", icon="ASSET_MANAGER")
        layout.prop(self, "generate_previews", icon="RESTRICT_RENDER_OFF")

    def do_on_asset(self, asset):
        if asset.asset_data and not self.overwrite:
            return
        asset.asset_mark()
        ensure_asset_uuid(asset)
        if self.generate_previews and can_preview_be_generated(asset):
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
