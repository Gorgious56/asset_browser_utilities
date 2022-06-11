from asset_browser_utilities.module.asset.tool import is_asset


def assert_that_id_is_an_asset(_id):
    assert is_asset(_id), f"'{repr(_id)}' should be an asset."


def assert_that_id_is_not_an_asset(_id):
    assert not is_asset(_id), f"'{repr(_id)}' should NOT be an asset."
