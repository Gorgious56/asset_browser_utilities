import bpy
from asset_browser_utilities.core.test.prop import TestOperator
from asset_browser_utilities.module.catalog.operator.move_to import CatalogMovetoBatchExecute

from asset_browser_utilities.module.asset.tool import all_assets
from asset_browser_utilities.module.catalog.test.tool import CATALOG_TO_UUID, assert_that_asset_is_in_catalog


def test_moving_all_assets_from_catalog_a_to_catalog_b(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=True,
        op_name="catalog_move_op",
        logic_class=CatalogMovetoBatchExecute,
    )

    bpy.ops.wm.open_mainfile(filepath=str(filepath))

    test_op.op_props.catalog.allow = True
    test_op.op_props.catalog.active = True
    test_op.op_props.catalog.catalog = CATALOG_TO_UUID

    test_op.execute()

    for asset in all_assets():
        assert_that_asset_is_in_catalog(asset, CATALOG_TO_UUID)
