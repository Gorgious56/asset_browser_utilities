import bpy

from asset_browser_utilities.core.test.tool import (
    execute_logic,
    get_asset_filter_settings,
    set_library_export_source,
    setup_and_get_current_operator,
)

from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.module.author.set import AuthorSetBatchExecute

from asset_browser_utilities.module.asset.tool import all_assets, all_assets_container_and_name


def setup_current_operator_():
    return setup_and_get_current_operator("author_set_op")


def test_setting_author_on_all_assets(filepath):
    bpy.ops.wm.open_mainfile(filepath=str(filepath))

    set_library_export_source(LibraryType.FileCurrent.value)

    asset_filter_settings = get_asset_filter_settings()
    asset_filter_settings.filter_assets = True
    asset_filter_settings.filter_types.types_global_filter = False

    op_props = setup_current_operator_()
    for author in ("test_author", ""):
        op_props.author = author

        execute_logic(AuthorSetBatchExecute)

        for asset in all_assets():
            assert (
                asset.asset_data.author == author
            ), f"{repr(asset)}'s author should be '{author}' instead of '{asset.asset_data.author}'"
