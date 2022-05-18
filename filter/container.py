from collections import defaultdict
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

    def filter_by_selection(self, filter_selection):
        if not filter_selection.active:
            return
        if filter_selection.asset_browser:
            selected_ids_in_asset_browser = set(asset_file.local_id for asset_file in bpy.context.selected_asset_files)
        if filter_selection.view_3d:
            selected_ids_in_viewport = set(o for o in bpy.context.visible_objects if o.select_get())
        selected_ids = selected_ids_in_asset_browser.union(selected_ids_in_viewport)
        for items in self.assets.values():
            for i in range(len(items) - 1, -1, -1):
                if items[i] not in selected_ids:
                    items.pop(i)

    @property
    def all_assets(self):
        for assets in self.assets.values():
            yield from assets
