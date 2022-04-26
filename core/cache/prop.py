from asset_browser_utilities.core.operator.operation import OperationSettings
from bpy.types import PropertyGroup
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.filter.main import AssetFilterSettings
from asset_browser_utilities.library.prop import LibraryExportSettings
from asset_browser_utilities.catalog.prop import CatalogExportSettings
# from asset_browser_utilities.asset.import_.prop import CacheAssetPaths
from asset_browser_utilities.tag.smart_tag import SmartTagPG


class Cache(PropertyGroup):
    library_settings: PointerProperty(type=LibraryExportSettings)
    operation_settings: PointerProperty(type=OperationSettings)
    asset_filter_settings: PointerProperty(type=AssetFilterSettings)
    # asset_paths: PointerProperty(type=CacheAssetPaths)
    catalog_settings: PointerProperty(type=CatalogExportSettings)
    smart_tag_settings: PointerProperty(type=SmartTagPG)

    show: BoolProperty()

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
    
    def draw(self, layout, context, header=None, rename=False):
        if header is None:
            header = self.name
        row = layout.row(align=True)
        if rename:
            row.prop(self, "name")
        row.prop(self, "show", toggle=True, text=header)
        if self.show:
            for attr in self.__annotations__:
                default_setting = getattr(self, attr)
                if hasattr(default_setting, "draw"):
                    default_setting.draw(layout, context)
        
