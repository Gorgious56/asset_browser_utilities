from asset_browser_utilities.core.operator.operation import OperationSettings
from bpy.types import PropertyGroup
from bpy.props import PointerProperty

from asset_browser_utilities.filter.main import AssetFilterSettings
from asset_browser_utilities.library.prop import LibraryExportSettings
from asset_browser_utilities.catalog.prop import CatalogExportSettings
from asset_browser_utilities.asset.import_.prop import CacheAssetPaths
from asset_browser_utilities.tag.smart_tag import SmartTagPG


class Cache(PropertyGroup):
    library_settings: PointerProperty(type=LibraryExportSettings)
    operation_settings: PointerProperty(type=OperationSettings)
    asset_filter_settings: PointerProperty(type=AssetFilterSettings)
    asset_paths: PointerProperty(type=CacheAssetPaths)
    catalog_settings: PointerProperty(type=CatalogExportSettings)
    smart_tag_settings: PointerProperty(type=SmartTagPG)

    def set(self, value):
        for prop_name in self.__annotations__:
            prop = getattr(self, prop_name)
            if isinstance(value, type(prop)):
                prop.copy(value)

    def get(self, _type):
        for prop_name in self.__annotations__:
            prop = getattr(self, prop_name)
            if isinstance(prop, _type):
                return prop
