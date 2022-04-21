from asset_browser_utilities.core.preferences.helper import CacheMapping
from bpy.types import PropertyGroup
from bpy.props import StringProperty


class CatalogExportSettings(PropertyGroup, CacheMapping):
    CACHE_MAPPING = "catalog_settings"

    path: StringProperty()
