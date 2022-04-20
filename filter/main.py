from asset_browser_utilities.core.ui.menu.helper import is_current_file
from bpy.types import PropertyGroup
from bpy.props import BoolProperty, PointerProperty

from asset_browser_utilities.filter.type import FilterTypes, get_object_types, get_types
from asset_browser_utilities.filter.name import FilterName
from asset_browser_utilities.filter.selection import FilterSelection
from asset_browser_utilities.filter.container import AssetContainer
from asset_browser_utilities.catalog.prop import FilterCatalog
from asset_browser_utilities.catalog.helper import CatalogsHelper
from asset_browser_utilities.core.helper import copy_simple_property_group


class AssetFilterSettings(PropertyGroup):
    filter_types: PointerProperty(type=FilterTypes)
    filter_name: PointerProperty(type=FilterName)
    filter_selection: PointerProperty(type=FilterSelection)
    filter_catalog: PointerProperty(type=FilterCatalog)
    filter_catalog_allow: BoolProperty(default=False)
    filter_assets: BoolProperty(
        default=False,
        name="Only Existing Assets",
        description="""Only Export Existing Assets.
If unchecked, items that are not yet assets will be exported and marked as assets in the target file""",
    )
    filter_assets_allow: BoolProperty(default=False)

    def init(self, context, filter_selection=False, filter_assets=False):
        self.filter_selection.allow = filter_selection and is_current_file(context)
        self.filter_assets_allow = filter_assets
        self.filter_assets = filter_assets
        self.filter_catalog_allow = filter_assets

    def get_objects_that_satisfy_filters(self):
        data_containers = list(self.filter_types.types) if self.filter_types.types_global_filter else [t[0] for t in get_types()]
        object_types = (
            list(self.filter_types.types_object)
            if (self.filter_types.types_object_filter and self.filter_types.types_global_filter)
            else [t[0] for t in get_object_types()]
        )
        asset_container = AssetContainer(data_containers, object_types)
        if self.filter_assets:
            asset_container.filter_assets()
            if self.filter_catalog.active:
                asset_container.filter_by_catalog(self.filter_catalog.catalog)
        if self.filter_name.active:
            asset_container.filter_by_name(self.filter_name.method, self.filter_name.value)
        if self.filter_selection.active:
            asset_container.filter_by_selection(self.filter_selection.source)
        return list(asset_container.all_assets)

    def draw(self, layout):
        self.filter_selection.draw(layout)
        self.filter_types.draw(layout)
        self.filter_name.draw(layout)
        if self.filter_catalog_allow:
            self.filter_catalog.draw(layout)

    def copy(self, other):
        copy_simple_property_group(other, self)
        copy_simple_property_group(other.filter_types, self.filter_types)
        copy_simple_property_group(other.filter_name, self.filter_name)
        copy_simple_property_group(other.filter_selection, self.filter_selection)
        helper = CatalogsHelper()
        if helper.has_catalogs:
            copy_simple_property_group(other.filter_catalog, self.filter_catalog)
