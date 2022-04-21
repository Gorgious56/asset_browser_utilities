from collections import defaultdict
import bpy

from asset_browser_utilities.filter.selection import Sources as SelectionSources


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
                if not items[i].asset_data.catalog_id == uuid:
                    items.pop(i)

    def filter_by_name(self, method, value):
        for items in self.assets.values():
            for i in range(len(items) - 1, -1, -1):
                name = items[i].name
                if method == "Prefix":
                    if not name.startswith(value):
                        items.pop(i)
                elif method == "Contains":
                    if value not in name:
                        items.pop(i)
                elif method == "Suffix":
                    if not name.endswith(value):
                        items.pop(i)


    def filter_by_selection(self, source):
        if source == SelectionSources.ASSET_BROWSER:
            selected_ids = [asset_file.local_id for asset_file in bpy.context.selected_asset_files]
        elif source == SelectionSources.OUTLINER:
            pass
        elif source == SelectionSources.VIEW_3D:
            selected_ids = [o for o in bpy.context.visible_objects if o.select_get()]
        for items in self.assets.values():
            for i in range(len(items) - 1, -1, -1):
                if items[i] not in selected_ids:
                    items.pop(i)
            
        

    @property
    def all_assets(self):
        for assets in self.assets.values():
            yield from assets
