from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.library.tool import append_asset
from asset_browser_utilities.core.filter.main import AssetFilterSettings

from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.library.prop import LibraryExportSettings
from asset_browser_utilities.core.library.tool import get_files_in_folder
from asset_browser_utilities.module.asset.prop import SelectedAssetRepresentations
from asset_browser_utilities.core.filter.type import get_types
import bpy
from bpy.types import Operator, PropertyGroup
from bpy.types import Operator
from bpy.props import PointerProperty

from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps


class AssetImportOperatorProperties(PropertyGroup, BaseOperatorProps):
    link_type: bpy.props.EnumProperty(
        items=(
            ("Append",) * 3,
            ("Link",) * 3,
        )
    )
    source: bpy.props.EnumProperty(
        name="Source",
        items=(
            ("Asset Browser Selection",) * 3,
            # ("Asset Library",) * 3,
        ),
    )

    def draw(self, layout, context=None):
        layout.prop(self, "link_type", text="")
        box = layout.box()
        box.prop(self, "source", text="")
        if self.source == "Asset Library":
            asset_library_settings = get_from_cache(LibraryExportSettings)
            asset_library_settings.draw_asset_library(box)

    def run_in_file(self, attributes=None):
        if self.source == "Asset Browser Selection":
            selected_asset_files_prop = get_from_cache(SelectedAssetRepresentations)
            for asset_representation in selected_asset_files_prop.assets:
                if asset_representation.is_local:
                    continue
                name_filter = get_from_cache(AssetFilterSettings).filter_name
                if not name_filter.filter(asset_representation.name):
                    continue
                asset = append_asset(
                    asset_representation.full_library_path,
                    asset_representation.id_type,
                    asset_representation.name,
                    link=self.link_type == "Link",
                )
                Logger.display(f"{self.link_type}ed {repr(asset)} from {asset_representation.full_library_path}")
        elif self.source == "Asset Library":
            return
            asset_library_settings = get_from_cache(LibraryExportSettings)
            asset_library_path = asset_library_settings.library_user_path
            blend_files = get_files_in_folder(asset_library_path, recursive=True)
            for blend_file in blend_files:
                with bpy.data.libraries.load(str(blend_file), assets_only=True, link=self.link_type == "Link") as (
                    data_from,
                    data_to,
                ):
                    filter_types = get_from_cache(AssetFilterSettings).filter_types
                    blend_data_names = (
                        list(self.filter_types.types)
                        if filter_types.types_global_filter
                        else [t[0] for t in get_types()]
                    )
                    for blend_data_name in blend_data_names:
                        pass


class ABU_OT_asset_mark(Operator, BatchFolderOperator):
    bl_idname: str = "abu.asset_import"
    bl_label: str = "Batch Import Assets"
    bl_description: str = "Batch Import Assets"

    operator_settings: PointerProperty(type=AssetImportOperatorProperties)
    ui_library = LibraryType.FileCurrent.value

    def invoke(self, context, event):
        return self._invoke(context, filter_selection=False)
