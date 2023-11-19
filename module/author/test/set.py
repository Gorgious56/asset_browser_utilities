from asset_browser_utilities.core.test.prop import TestOperator

from asset_browser_utilities.module.asset.tool import all_assets


def test_setting_author_on_all_assets(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=True,
    )

    for author in ("test_author", ""):
        test_op.op_props.author = author
        test_op.execute()

        for asset in all_assets():
            assert (
                asset.author == author
            ), f"{repr(asset)}'s author should be '{author}' instead of '{asset.asset_data.author}'"
