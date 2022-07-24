from pathlib import Path
from asset_browser_utilities.module.catalog.tool import CatalogsHelper
from asset_browser_utilities.core.cache.tool import get_current_operator_properties, get_from_cache
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.library.prop import LibraryExportSettings, LibraryType
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, PointerProperty, BoolProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator


class CatalogSortLikeFoldersBatchExecute(BatchExecute):
    def __init__(self):
        super().__init__()
        current_op = get_current_operator_properties()

        self.library_user_path = get_from_cache(LibraryExportSettings).library_user_path
        self.catalog_map = {}
        cat_helper = CatalogsHelper()
        for filepath in self.blends:
            try:
                catalog_tree = Path(str(filepath).replace(self.library_user_path, "")).parents[
                    1 if current_op.are_assets_in_subfolders else 0
                ]
            except IndexError:
                continue
            else:
                if str(catalog_tree) == ".":
                    continue
                uuid = cat_helper.ensure_or_create_catalog_definition(catalog_tree)
                self.catalog_map[filepath] = uuid

    def execute_one_file_and_the_next_when_finished(self):
        try:
            uuid = self.catalog_map[self.blend]
        except KeyError:
            pass
        else:
            changed_file = False
            for asset in self.assets:
                Logger.display(f"{repr(asset)} has been moved to catalog {uuid}")
                asset_data = asset.asset_data
                if asset_data.catalog_id != uuid:
                    asset_data.catalog_id = uuid
                    changed_file = True
            if changed_file:
                self.save_file()
        self.execute_next_blend()


class CatalogSortLikeFoldersOperatorProperties(PropertyGroup):
    are_assets_in_subfolders: BoolProperty(
        description="Check this if each asset is located in its own individual subfolder",
        default=False,
    )

    def draw(self, layout, context=None):
        layout.prop(self, "are_assets_in_subfolders", text="Assets are contained in individual folders")


class ABU_OT_sort_catalogs_like_folders(Operator, BatchFolderOperator):
    ui_library = (LibraryType.UserLibrary.value, LibraryType.FolderExternal.value)
    bl_idname = "abu.sort_catalogs_like_folders"
    bl_label = "Create Folder Structure"

    operator_settings: PointerProperty(type=CatalogSortLikeFoldersOperatorProperties)
    logic_class = CatalogSortLikeFoldersBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
