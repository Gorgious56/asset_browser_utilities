import bpy

from asset_browser_utilities.core.test.tool import execute_logic

from asset_browser_utilities.core.filter.type import get_types
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.module.asset.operator.unmark import AssetUnmarkBatchExecute

from asset_browser_utilities.module.asset.tool import get_asset_filer_settings, get_library_export_settings, is_asset


def test_unmarking_all_assets_in_current_file(filepath):
    bpy.ops.wm.open_mainfile(filepath=str(filepath))

    get_library_export_settings().source = LibraryType.FileCurrent.value

    asset_filter_settings = get_asset_filer_settings()
    asset_filter_settings.filter_assets = False
    asset_filter_settings.filter_types.types_global_filter = False

    execute_logic(AssetUnmarkBatchExecute)

    supported_asset_types = [a_t[0] for a_t in get_types()]
    for d in dir(bpy.data):
        container = getattr(bpy.data, d)
        if "bpy_prop_collection" in str(type(container)):
            if d in supported_asset_types:
                for asset in container:
                    assert not is_asset(asset), f"'bpy.data.{d}.{asset.name}' should not be an asset."
