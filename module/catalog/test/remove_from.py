import bpy

from asset_browser_utilities.core.test.tool import (
    execute_logic,
    get_asset_filter_settings,
    set_library_export_source,
    setup_and_get_current_operator,
)

from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.module.catalog.operator.remove_from import CatalogRemoveFromBatchExecute


from asset_browser_utilities.module.asset.tool import all_assets
from asset_browser_utilities.module.catalog.test.tool import (
    CATALOG_FROM_UUID,
    CATALOG_TO_UUID,
    all_assets_in_specific_catalog_container_and_name,
    assert_that_asset_is_in_catalog,
)


def setup_and_get_current_operator_():
    return setup_and_get_current_operator("catalog_remove_op")


def test_removing_all_assets_from_call_catalogs(filepath):
    bpy.ops.wm.open_mainfile(filepath=str(filepath))

    set_library_export_source(LibraryType.FileCurrent.value)

    asset_filter_settings = get_asset_filter_settings()
    asset_filter_settings.filter_assets = True
    asset_filter_settings.filter_types.types_global_filter = False

    op_props = setup_and_get_current_operator_()
    op_props.filter = False
    execute_logic(CatalogRemoveFromBatchExecute)

    for asset in all_assets():
        assert_that_asset_is_in_catalog(asset, "00000000-0000-0000-0000-000000000000")


def test_removing_all_assets_from_a_specific_catalog(filepath):
    bpy.ops.wm.open_mainfile(filepath=str(filepath))

    set_library_export_source(LibraryType.FileCurrent.value)

    asset_filter_settings = get_asset_filter_settings()
    asset_filter_settings.filter_assets = True
    asset_filter_settings.filter_types.types_global_filter = False

    all_assets_in_from_catalog = all_assets_in_specific_catalog_container_and_name(CATALOG_FROM_UUID)
    all_assets_in_to_catalog = all_assets_in_specific_catalog_container_and_name(CATALOG_TO_UUID)

    op_props = setup_and_get_current_operator_()
    op_props.filter = True
    op_props.catalog.allow = op_props.catalog.active = True
    op_props.catalog.catalog = CATALOG_FROM_UUID

    execute_logic(CatalogRemoveFromBatchExecute)

    for container, name in all_assets_in_from_catalog:
        asset = getattr(bpy.data, container)[name]
        assert_that_asset_is_in_catalog(asset, "00000000-0000-0000-0000-000000000000")
    for container, name in all_assets_in_to_catalog:
        asset = getattr(bpy.data, container)[name]
        assert_that_asset_is_in_catalog(asset, CATALOG_TO_UUID)

