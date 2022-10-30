import bpy
from asset_browser_utilities.core.test.prop import TestOperator

from asset_browser_utilities.module.catalog.operator.remove_empty import CatalogRemoveEmptyBatchExecute

from asset_browser_utilities.module.catalog.tool import all_catalogs
from asset_browser_utilities.module.asset.tool import all_assets


def test_removing_all_empty_catalogs(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=False,
        logic_class=CatalogRemoveEmptyBatchExecute,
    )

    catalogs_uuids = set(cat[0] for cat in all_catalogs())
    # /!\ Assets with no catalog have a catalog uuid of '00000000-0000-0000-0000-000000000000'
    catalogs_uuids_assets = set(asset.catalog_id for asset in all_assets())
    assert len(catalogs_uuids) + 1 > len(catalogs_uuids_assets)

    test_op.execute()

    catalogs_uuids = [cat[0] for cat in all_catalogs()]
    assert len(catalogs_uuids) + 1 == len(catalogs_uuids_assets)


def test_removing_an_empty_catalog_by_name(filepath):
    # TODO
    pass
