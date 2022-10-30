import bpy
from asset_browser_utilities.core.test.prop import TestOperator

from asset_browser_utilities.module.catalog.operator.remove_from import CatalogRemoveFromBatchExecute


from asset_browser_utilities.module.asset.tool import all_assets
from asset_browser_utilities.module.catalog.test.tool import (
    CATALOG_FROM_UUID,
    CATALOG_TO_UUID,
    all_assets_in_specific_catalog_container_and_name,
    assert_that_asset_is_in_catalog,
)


def test_removing_all_assets_from_call_catalogs(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=True,
        logic_class=CatalogRemoveFromBatchExecute,
    )

    test_op.op_props.filter = False

    test_op.execute()

    for asset in all_assets():
        assert_that_asset_is_in_catalog(asset, "00000000-0000-0000-0000-000000000000")


def test_removing_all_assets_from_a_specific_catalog(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=True,
        logic_class=CatalogRemoveFromBatchExecute,
    )

    all_assets_in_from_catalog = all_assets_in_specific_catalog_container_and_name(CATALOG_FROM_UUID)
    all_assets_in_to_catalog = all_assets_in_specific_catalog_container_and_name(CATALOG_TO_UUID)

    test_op.op_props.filter = True
    test_op.op_props.catalog.allow = True
    test_op.op_props.catalog.active = True
    test_op.op_props.catalog.catalog = CATALOG_FROM_UUID

    test_op.execute()

    for container, name in all_assets_in_from_catalog:
        asset = getattr(bpy.data, container)[name].asset_data
        assert_that_asset_is_in_catalog(asset, "00000000-0000-0000-0000-000000000000")
    for container, name in all_assets_in_to_catalog:
        asset = getattr(bpy.data, container)[name].asset_data
        assert_that_asset_is_in_catalog(asset, CATALOG_TO_UUID)
