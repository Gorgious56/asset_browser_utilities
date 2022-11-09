from bpy.types import PropertyGroup
from bpy.props import PointerProperty

from asset_browser_utilities.core.filter.type import FilterTypes, get_object_types, get_types
from asset_browser_utilities.core.filter.name import FilterName
from asset_browser_utilities.core.filter.selection import FilterSelection
from asset_browser_utilities.core.filter.container import AssetContainer
from asset_browser_utilities.core.filter.catalog import FilterCatalog
from asset_browser_utilities.core.filter.asset import FilterAssets
from asset_browser_utilities.core.filter.tag import FilterTag
from asset_browser_utilities.core.filter.author import FilterAuthor
from asset_browser_utilities.core.tool import copy_simple_property_group
from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.library.prop import LibraryExportSettings, LibraryType


class AssetFilterSettings(PropertyGroup):
    filter_types: PointerProperty(type=FilterTypes)
    filter_name: PointerProperty(type=FilterName)
    filter_selection: PointerProperty(type=FilterSelection)
    filter_catalog: PointerProperty(type=FilterCatalog)
    filter_assets: PointerProperty(type=FilterAssets)
    filter_tag: PointerProperty(type=FilterTag)
    filter_author: PointerProperty(type=FilterAuthor)

    def init_asset_filter_settings(
        self,
        filter_selection=False,
        filter_assets=False,
        filter_types=True,
    ):
        self.filter_selection.init(
            allow=filter_selection and get_from_cache(LibraryExportSettings).source == LibraryType.FileCurrent.value
        )
        self.filter_tag.init()
        self.filter_assets.only_assets = filter_assets
        self.filter_catalog.allow = filter_assets
        self.filter_types.allow = filter_types

    def get_objects_that_satisfy_filters(self):
        data_containers = (
            list(self.filter_types.types) if self.filter_types.types_global_filter else [t[0] for t in get_types()]
        )
        object_types = (
            list(self.filter_types.types_object)
            if (self.filter_types.types_object_filter and self.filter_types.types_global_filter)
            else [t[0] for t in get_object_types()]
        )
        asset_container = AssetContainer(data_containers, object_types)
        if self.filter_assets.only_assets:
            asset_container.filter_assets()
            if self.filter_catalog.active:
                uuid = (
                    "00000000-0000-0000-0000-000000000000"
                    if self.filter_catalog.unassigned
                    else self.filter_catalog.catalog_uuid
                )
                asset_container.filter_by_catalog(uuid)
            if self.filter_tag.active:
                asset_container.filter_by_tags(self.filter_tag.tags.get_valid_tags(), self.filter_tag.orand)
            if self.filter_author.active:
                asset_container.filter_by_author(self.filter_author.name)

        if self.filter_name.active:
            asset_container.filter_by_name(
                self.filter_name.method,
                self.filter_name.value,
                self.filter_name.case_sensitive,
            )
        if self.filter_selection.active:
            asset_container.filter_by_selection(self.filter_selection)
        return list(asset_container.all_assets)

    def draw(self, layout, context):
        box = layout.box()
        self.filter_selection.draw(box)
        if self.filter_types.allow:
            self.filter_types.draw(box)
        self.filter_name.draw(box, name_override="Assets")

        if self.filter_assets.only_assets:
            self.filter_catalog.draw(box, context)
            self.filter_tag.draw(box, context)
            self.filter_author.draw(box, context)

    def copy_from(self, other):
        # Other is the source, self is the target
        copy_simple_property_group(other, self)
        copy_simple_property_group(other.filter_assets, self.filter_assets)
        copy_simple_property_group(other.filter_types, self.filter_types)
        copy_simple_property_group(other.filter_name, self.filter_name)
        copy_simple_property_group(other.filter_selection, self.filter_selection)
        copy_simple_property_group(other.filter_catalog, self.filter_catalog)

    @staticmethod
    def are_objects_filtered():
        filter_types = get_from_cache(AssetFilterSettings).filter_types
        return "objects" in filter_types.types or not filter_types.types_global_filter

    @staticmethod
    def are_mesh_objects_filtered():
        filter_types = get_from_cache(AssetFilterSettings).filter_types
        return ("objects" in filter_types.types or not filter_types.types_global_filter) and (
            "MESH" in filter_types.types_object or not filter_types.types_object_filter
        )
