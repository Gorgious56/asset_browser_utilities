from collections import defaultdict
import bpy

from asset_browser_utilities.prop.filter.selection import Sources as SelectionSources


class AssetContainer:
    def __init__(self, filter_types=None):
        self.assets = defaultdict(list)
        self.assets_filter = defaultdict(bool)
        if filter_types is not None:
            self.populate_assets(filter_types)

    def populate_assets(self, filter_types):
        for data_name in filter_types:
            self.assets_filter[data_name] = True
            type_container = self.assets[data_name]
            items = getattr(bpy.data, data_name)
            for item in items:
                type_container.append(item)

    def filter_assets(self):
        for items in self.assets.values():
            for i in range(len(items) - 1, -1, -1):
                if not items[i].asset_data:
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

    def filter_objects_by_selection(self, source):
        objects = self.assets["objects"]
        for i in range(len(objects) - 1, -1, -1):
            if not objects[i].select_get():
                objects.pop(i)

    def filter_materials_by_selection(self, source):
        materials = self.assets["materials"]
        if self.assets_filter["objects"]:
            objects = self.assets["objects"]
        else:
            objects = [o for o in bpy.data.objects if o.select_get()]
        for i in range(len(materials) - 1, -1, -1):
            mat = materials[i]
            found = False
            for obj in objects:
                if mat.name in [m_s.name for m_s in obj.material_slots]:
                    found = True
                    break
            if not found:
                materials.pop(i)

    @property
    def all_assets(self):
        all_assets = []
        for assets in self.assets.values():
            all_assets.extend(assets)
        return all_assets
