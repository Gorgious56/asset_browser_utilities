from bpy.types import PropertyGroup
from bpy.props import PointerProperty

from asset_browser_utilities.filter.main import AssetFilterSettings
from asset_browser_utilities.library.path import LibraryExportSettings


class Cache(PropertyGroup):
    library_settings: PointerProperty(type=LibraryExportSettings)
    asset_filter_settings: PointerProperty(type=AssetFilterSettings)

    def set(self, value):
        if isinstance(value, LibraryExportSettings):
            self.library_settings.copy(value)
        elif isinstance(value, AssetFilterSettings):
            self.asset_filter_settings.copy(value)

    def get(self, _type):
        if isinstance(self.library_settings, _type):
            return self.library_settings
        elif isinstance(self.asset_filter_settings, _type):
            return self.asset_filter_settings
