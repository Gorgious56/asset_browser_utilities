import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchFolderOperator
from asset_browser_utilities.core.cache.tool import get_current_operator_properties, get_from_cache
from asset_browser_utilities.core.console import command_line_execute_base
from asset_browser_utilities.core.filter.main import AssetFilterSettings
from asset_browser_utilities.core.file.save import save_file
from asset_browser_utilities.core.library.prop import LibraryExportSettings, LibraryType

from asset_browser_utilities.module.preview.tool import can_preview_be_generated
from asset_browser_utilities.module.library.tool import ensure_asset_uuid


def run_in_file():
    assets = get_from_cache(AssetFilterSettings).get_objects_that_satisfy_filters()
    if not assets:
        return
    operator_properties = get_current_operator_properties()
    for asset in assets:
        if asset.asset_data and not operator_properties.overwrite:
            continue
        asset.asset_mark()
        ensure_asset_uuid(asset)
        if operator_properties.generate_previews and can_preview_be_generated(asset):
            asset.asset_generate_preview()
        Logger.display(f"{bpy.data.filepath}\\{repr(asset)} marked")


class CommandLineExecute(command_line_execute_base.CommandLineExecuteBase):
    def run(self):
        run_in_file()
        if get_current_operator_properties().generate_previews:
            while bpy.app.is_job_running("RENDER_PREVIEW"):
                pass
        save_file()
        quit()


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

    def draw(self, layout, context=None):
        layout.prop(self, "overwrite", icon="ASSET_MANAGER")
        layout.prop(self, "generate_previews", icon="RESTRICT_RENDER_OFF")


class ABU_OT_asset_mark(Operator, BatchFolderOperator):
    bl_idname: str = "abu.asset_mark"
    bl_label: str = "Batch Mark Assets"
    bl_description: str = "Batch Mark Assets"
    INTERVAL_PREVIEW = 0.05

    operator_settings: PointerProperty(type=AssetMarkOperatorProperties)
    run_in_file = run_in_file
    file_for_command = __file__

    def invoke(self, context, event):
        return self._invoke(context)

    def execute(self, context):
        bpy.ops.wm.save_userpref()
        if get_from_cache(LibraryExportSettings).source == LibraryType.FileCurrent.value:
            ABU_OT_asset_mark.run_in_file()
        else:
            self.run_in_threads()
        return {"FINISHED"}
