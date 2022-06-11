from asset_browser_utilities.core.test.prop import TestOperator

from asset_browser_utilities.module.description.set import DescriptionSetBatchExecute

from asset_browser_utilities.module.asset.tool import all_assets


def assert_that_an_asset_description_matches(asset, description):
    assert (
        asset.asset_data.description == description
    ), f"{repr(asset)}'s description should be '{description}' instead of '{asset.asset_data.description}'"


def test_setting_author_on_all_assets(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=True,
        op_name="description_set_op",
        logic_class=DescriptionSetBatchExecute,
    )
    for description in ("test_descr", ""):
        test_op.op_props.description = description
        test_op.execute()

        for asset in all_assets():
            assert_that_an_asset_description_matches(asset, description)
