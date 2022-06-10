from asset_browser_utilities.core.log.logger import Logger
import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.core.cache.tool import get_current_operator_properties


class AssetMarkBatchExecute(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        if not self.assets:
            self.execute_next_blend()
            return
        operator_properties = get_current_operator_properties()
        for asset in self.assets:
            if asset.asset_data and not operator_properties.overwrite:
                Logger.display(f"Asset '{asset.name}' already marked")
                continue
            asset.asset_mark()
            if operator_properties.generate_previews:
                asset.asset_generate_preview()
            Logger.display(f"Asset '{asset.name}' marked")

        if operator_properties.generate_previews:
            bpy.app.timers.register(self.sleep_until_previews_are_done_and_execute_next_file)
        else:
            self.save_file()
            self.execute_next_blend()


class AssetMarkOperatorProperties(PropertyGroup):
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

    def draw(self, layout):
        layout.prop(self, "overwrite", icon="ASSET_MANAGER")
        row = layout.row(align=True)
        row.prop(self, "generate_previews", icon="RESTRICT_RENDER_OFF")


class ABU_OT_batch_mark(Operator, BatchFolderOperator):
    "Batch Mark Assets"
    bl_idname = "abu.batch_mark"
    bl_label = "Batch Mark Assets"
    bl_options = {"UNDO"}

    operator_settings: PointerProperty(type=AssetMarkOperatorProperties)
    logic_class = AssetMarkBatchExecute

    def invoke(self, context, event):
        return self._invoke(context)
