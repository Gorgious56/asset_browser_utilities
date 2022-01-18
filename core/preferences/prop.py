from bpy.types import PropertyGroup
from bpy.props import PointerProperty

from asset_browser_utilities.filter.main import AssetFilterSettings
from asset_browser_utilities.library.prop import LibraryExportSettings


class Cache(PropertyGroup):
    library_settings: PointerProperty(type=LibraryExportSettings)
    asset_filter_settings: PointerProperty(type=AssetFilterSettings)

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
