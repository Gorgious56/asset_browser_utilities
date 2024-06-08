from collections import defaultdict
from pathlib import Path
from asset_browser_utilities.module.asset.prop import SelectedAssetRepresentations
from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.filter.name import FilterName
from asset_browser_utilities.core.filter.type import get_types
from asset_browser_utilities.core.library.prop import LibraryExportSettings, LibraryType
import bpy


class AssetContainer:
    def __init__(self, filter_types=None, filter_object_types=None):
        self.assets = defaultdict(list)
        self.assets_filter = defaultdict(bool)
        if filter_types is not None:
            self.populate_assets(filter_types, filter_object_types)

    def populate_assets(self, filter_types, filter_object_types):
        for data_name in filter_types:
            self.assets_filter[data_name] = True
            type_container = self.assets[data_name]
            items = getattr(bpy.data, data_name)
            if data_name == "objects" and filter_object_types is not None:
                for item in items:
                    if item.type in filter_object_types:
                        type_container.append(item)
            else:
                for item in items:
                    type_container.append(item)

    def filter_assets(self):
        for items in self.assets.values():
            for i in range(len(items) - 1, -1, -1):
                if not items[i].asset_data:
                    items.pop(i)

    def filter_by_catalog(self, uuid):
        for items in self.assets.values():
            for i in range(len(items) - 1, -1, -1):
                if items[i].asset_data.catalog_id != uuid:
                    items.pop(i)

    def filter_by_author(self, name):
        for items in self.assets.values():
            for i in range(len(items) - 1, -1, -1):
                if items[i].asset_data.author != name:
                    items.pop(i)

    def filter_by_tags(self, tags, orand):
        for items in self.assets.values():
            for i in range(len(items) - 1, -1, -1):
                asset_tag_names = [t.name for t in items[i].asset_data.tags]
                if orand == "AND":
                    for tag in tags:
                        if tag not in asset_tag_names:
                            items.pop(i)
                            break
                elif orand == "OR":
                    for tag in tags:
                        if tag in asset_tag_names:
                            break
                    else:
                        items.pop(i)

    def filter_by_name(self, method, value, case_sensitive):
        for items in self.assets.values():
            for i in range(len(items) - 1, -1, -1):
                name = items[i].name
                if not FilterName.filter_static(name, method, value, case_sensitive):
                    items.pop(i)

    def filter_by_selection(self, filter_selection):
        if not filter_selection.active:
            return
        selected_ids = set()
        is_library_current_file = get_from_cache(LibraryExportSettings).source == LibraryType.FileCurrent.value
        if filter_selection.selection_type == "Asset Browser":
            for asset_representation in get_from_cache(SelectedAssetRepresentations).assets:
                if (asset_representation.is_local and is_library_current_file) or Path(
                    asset_representation.full_library_path
                ) == Path(bpy.data.filepath):
                    selected_ids.add(getattr(bpy.data, asset_representation.directory)[asset_representation.name])
        elif filter_selection.selection_type == "3D Viewport":
            selected_ids.update(o for o in bpy.context.visible_objects if o.select_get())
        for items in self.assets.values():
            for i in range(len(items) - 1, -1, -1):
                if items[i] not in selected_ids:
                    items.pop(i)

    @property
    def all_assets(self):
        for assets in self.assets.values():
            yield from assets


def get_all_assets_in_file():
    asset_container = AssetContainer(filter_types=[t[0] for t in get_types()])
    asset_container.filter_assets()
    return asset_container.all_assets
