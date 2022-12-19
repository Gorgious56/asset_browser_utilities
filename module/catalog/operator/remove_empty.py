from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.filter.main import AssetFilterSettings
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.module.asset.tool import all_assets
from asset_browser_utilities.module.catalog.tool import CatalogsHelper


class CatalogRemoveEmptyBatchExecute(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        asset_uuids = set(asset.catalog_id for asset in all_assets())
        helper = CatalogsHelper()

        asset_filter_settings = get_from_cache(AssetFilterSettings)
        filter_name = asset_filter_settings.filter_name
        filter_func = lambda name: filter_name.filter(name) if filter_name.active else lambda: True

        catalogs = {cat[0]: cat[1] for cat in helper.get_catalogs() if filter_func(cat[1])}
        catalog_uuids = set(catalogs.keys())

        empty_catalogs = catalog_uuids.difference(asset_uuids)
        for empty_catalog_uuid in empty_catalogs:
            helper.remove_catalog_by_uuid(empty_catalog_uuid)
            Logger.display(f"Removed empty catalog '{catalogs[empty_catalog_uuid]}'")

        self.save_file()
        self.execute_next_file()


class CatalogRemoveEmptyOperatorProperties(PropertyGroup):
    pass


class ABU_OT_catalog_remove_empty(Operator, BatchFolderOperator):
    bl_idname = "abu.catalog_remove_empty"
    bl_label = "Batch Remove Empty Catalogs"

    operator_settings: PointerProperty(type=CatalogRemoveEmptyOperatorProperties)
    logic_class = CatalogRemoveEmptyBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=False, filter_type=False, filter_selection=False)
