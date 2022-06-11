import bpy

from asset_browser_utilities.core.test.tool import (
    execute_logic,
    get_asset_filter_settings,
    set_library_export_source,
    setup_and_get_current_operator,
)

from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.module.catalog.operator.move_to import CatalogMovetoBatchExecute


from asset_browser_utilities.module.asset.tool import all_assets
from asset_browser_utilities.module.catalog.test.tool import CATALOG_TO_UUID, assert_that_asset_is_in_catalog


def setup_and_get_current_operator_():
    return setup_and_get_current_operator("catalog_move_op")


def test_moving_all_assets_from_catalog_a_to_catalog_b(filepath):
    bpy.ops.wm.open_mainfile(filepath=str(filepath))

    set_library_export_source(LibraryType.FileCurrent.value)

    asset_filter_settings = get_asset_filter_settings()
    asset_filter_settings.filter_assets = True
    asset_filter_settings.filter_types.types_global_filter = False

    op_props = setup_and_get_current_operator_()
    op_props.catalog.allow = op_props.catalog.active = True
    op_props.catalog.catalog = CATALOG_TO_UUID

    execute_logic(CatalogMovetoBatchExecute)

    for asset in all_assets():
        assert_that_asset_is_in_catalog(asset, CATALOG_TO_UUID)
