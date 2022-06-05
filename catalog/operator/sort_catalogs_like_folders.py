from pathlib import Path
from asset_browser_utilities.catalog.tool import CatalogsHelper
from asset_browser_utilities.library.prop import LibraryExportSettings
import bpy.app.timers
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, PointerProperty, BoolProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator


class BatchExecuteOverride(BatchExecute):
    def __init__(self, operator, context):
        super().__init__(operator, context)

        self.library_user_path = LibraryExportSettings.get_from_cache().library_user_path
        self.catalog_map = {}
        cat_helper = CatalogsHelper()
        for filepath in self.blends:
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

    def execute_one_file_and_the_next_when_finished(self):
        cat_helper = CatalogsHelper()
        try:
            uuid = self.catalog_map[self.blend]
        except KeyError:
            pass
        else:
            for asset in self.assets:
                print(f"{asset.name} has been moved to catalog {uuid}")
                asset_data = asset.asset_data
                if asset_data.catalog_id != uuid:
                    asset_data.catalog_id = uuid
            self.save_file()
        self.execute_next_blend()


class OperatorProperties(PropertyGroup):
    are_assets_in_subfolders: BoolProperty(
        description="Check this if each asset is located in its own individual subfolder",
        default=True,
    )

    def draw(self, layout):
        layout.prop(self, "are_assets_in_subfolders", text="Assets are contained in individual folders")


class ABU_OT_sort_catalogs_like_folders(Operator, BatchFolderOperator):
    bl_idname = "abu.sort_catalogs_like_folders"
    bl_label = "Create Folder Structure"

    operator_settings: PointerProperty(type=OperatorProperties)
    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
