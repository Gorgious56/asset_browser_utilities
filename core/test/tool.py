from asset_browser_utilities.core.cache.tool import get_cache, get_current_operator_properties, get_from_cache
from asset_browser_utilities.core.operator.prop import CurrentOperatorProperty
from asset_browser_utilities.core.filter.main import AssetFilterSettings
from asset_browser_utilities.core.library.prop import LibraryExportSettings
from asset_browser_utilities.module.asset.prop import SelectedAssetFiles


def get_asset_filter_settings():
    return get_from_cache(AssetFilterSettings)


def get_library_export_settings():
    return get_from_cache(LibraryExportSettings)


def set_library_export_source(source):
    get_library_export_settings().source = source


def setup_and_get_current_operator(attr_name):
    prop = getattr(get_cache(), attr_name, None)
    if prop is None:
        return None
    get_from_cache(CurrentOperatorProperty).class_name = str(prop.__class__)
    return get_current_operator_properties()


def execute_logic(logic_class):
    logic = logic_class()
    logic.save_file = lambda: None
    logic.execute_next_blend()
