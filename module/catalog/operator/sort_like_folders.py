from pathlib import Path
from asset_browser_utilities.module.catalog.tool import CatalogsHelper
from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.library.prop import LibraryExportSettings, LibraryType
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, PointerProperty, BoolProperty

from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps


class CatalogSortLikeFoldersOperatorProperties(PropertyGroup, BaseOperatorProps):
    are_assets_in_subfolders: BoolProperty(
        description="Check this if each asset is located in its own individual subfolder",
        default=False,
    )

    def draw(self, layout, context=None):
        layout.prop(self, "are_assets_in_subfolders", text="Assets are contained in individual folders")

    def init(self):
        self.library_user_path = get_from_cache(LibraryExportSettings).library_user_path
        self.catalog_map = {}
        cat_helper = CatalogsHelper()
        for filepath in self.files:
            try:
                catalog_tree = Path(str(filepath).replace(self.library_user_path, "")).parents[
                    1 if self.are_assets_in_subfolders else 0
                ]
            except IndexError:
                continue
            else:
                if str(catalog_tree) == ".":
                    continue
                uuid = cat_helper.ensure_or_create_catalog_definition(catalog_tree)
                self.catalog_map[filepath] = uuid

    def run_in_file(self, attributes=None):
        try:
            uuid = self.catalog_map[self.file]
        except KeyError:
            pass
        else:
            changed_file = False
            for asset in self.get_assets():
                Logger.display(f"{repr(asset)} has been moved to catalog {uuid}")
                asset_data = asset.asset_data
                if asset_data.catalog_id != uuid:
                    asset_data.catalog_id = uuid
                    changed_file = True
            if changed_file:
                self.save_file()
        self.execute_next_file()


class ABU_OT_catalog_sort_like_folders(Operator, BatchFolderOperator):
    ui_library = (LibraryType.UserLibrary.value, LibraryType.FolderExternal.value)
    bl_idname = "abu.catalog_sort_like_folders"
    bl_label = "Create Folder Structure"

    operator_settings: PointerProperty(type=CatalogSortLikeFoldersOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
