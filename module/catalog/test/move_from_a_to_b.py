import bpy
from asset_browser_utilities.core.test.prop import TestOperator

from asset_browser_utilities.module.catalog.operator.move_from_a_to_b import CatalogMoveFromAToBBatchExecute

from asset_browser_utilities.module.catalog.test.tool import (
    all_assets_in_specific_catalog_container_and_name,
    CATALOG_FROM_UUID,
    CATALOG_TO_UUID,
    assert_that_asset_is_in_catalog,
)


def test_moving_all_assets_from_catalog_a_to_catalog_b(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=True,
        op_name="catalog_move_from_a_to_b_op",
        logic_class=CatalogMoveFromAToBBatchExecute,
    )

    all_assets_in_from_catalog = all_assets_in_specific_catalog_container_and_name(CATALOG_FROM_UUID)

    test_op.op_props.catalog_from.allow = True
    test_op.op_props.catalog_from.active = True
    test_op.op_props.catalog_from.catalog = CATALOG_FROM_UUID
    test_op.op_props.catalog_to.allow = True
    test_op.op_props.catalog_to.active = True
    test_op.op_props.catalog_to.catalog = CATALOG_TO_UUID

    test_op.execute()

    for container, name in all_assets_in_from_catalog:
        asset = getattr(bpy.data, container)[name]
        assert_that_asset_is_in_catalog(asset, CATALOG_TO_UUID)
