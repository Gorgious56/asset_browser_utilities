from bpy.types import PropertyGroup
from bpy.props import BoolProperty, PointerProperty

from asset_browser_utilities.prop.filter.type import FilterTypes
from asset_browser_utilities.prop.filter.name import FilterName
from asset_browser_utilities.prop.filter.selection import FilterSelection
from asset_browser_utilities.prop.filter.catalog import FilterCatalog
from asset_browser_utilities.prop.filter.container import AssetContainer
from asset_browser_utilities.helper.prop import copy_simple_property_group


class AssetFilterSettings(PropertyGroup):
    filter_types: PointerProperty(type=FilterTypes)
    filter_name: PointerProperty(type=FilterName)
    filter_selection: PointerProperty(type=FilterSelection)
    filter_catalog: PointerProperty(type=FilterCatalog)
    filter_assets: BoolProperty(
        default=False,
        name="Only Existing Assets",
        description="""Only Export Existing Assets.
If unchecked, items that are not yet assets will be exported and marked as assets in the target file""",
    )
    filter_assets_allow: BoolProperty(default=False)

    def init(self, filter_selection=False, filter_assets=False):
        self.filter_selection.allow = filter_selection
        self.filter_assets_allow = filter_assets
        self.filter_assets = filter_assets
        self.filter_types.init()

    def get_objects_that_satisfy_filters(self):
        asset_container = AssetContainer([item.name for item in self.filter_types.items if item.value])
        if self.filter_assets:
            asset_container.filter_assets()
            if self.filter_catalog.active:
                asset_container.filter_by_catalog(self.filter_catalog.catalog)
        if self.filter_name.active:
            asset_container.filter_by_name(self.filter_name.method, self.filter_name.value)
        if self.filter_selection.active:
            asset_container.filter_objects_by_selection(self.filter_selection.source)
            asset_container.filter_materials_by_selection(self.filter_selection.source)
        return asset_container.all_assets

    def draw(self, layout):
        self.filter_selection.draw(layout)
        self.filter_types.draw(layout)
        self.filter_name.draw(layout)
        self.filter_catalog.draw(layout)

    def copy(self, other):
        copy_simple_property_group(other.filter_name, self.filter_name)
        self.filter_types.copy(other.filter_types)
        copy_simple_property_group(other, self)
