from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.filter.main import AssetFilterSettings
from asset_browser_utilities.core.library.prop import LibraryExportSettings
import bpy


def ensure_object_is_not_asset(obj):
    obj.asset_clear()


def is_asset(obj):
    return obj.asset_data is not None


def all_assets():
    return [o.name for o in bpy.data.objects if is_asset(o)]


def get_asset_filer_settings():
    return get_from_cache(AssetFilterSettings)


def get_library_export_settings():
    return get_from_cache(LibraryExportSettings)
