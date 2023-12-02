import bpy
from bpy.types import PropertyGroup
from bpy.props import StringProperty, CollectionProperty, IntProperty, BoolProperty

from asset_browser_utilities.core.library.tool import get_blend_data_name_from_directory


class AssetRepresentation(PropertyGroup):
    full_library_path: StringProperty()
    id_type: StringProperty()
    directory: StringProperty()
    name: StringProperty()
    is_local: BoolProperty()


class SelectedAssetRepresentations(PropertyGroup):
    active_index: IntProperty()
    assets: CollectionProperty(type=AssetRepresentation)

    def init(self):
        self.assets.clear()
        self.active_index = -1

    def add_assets(self, asset_representations):
        for asset_representation in asset_representations:
            self.add_asset(asset_representation)

    def add_asset(self, asset_representation):
        new = self.assets.add()
        new.full_library_path = asset_representation.full_library_path
        new.id_type = asset_representation.id_type
        new.directory = get_blend_data_name_from_directory(new.id_type)
        new.name = asset_representation.name
        new.is_local = bool(asset_representation.local_id)

    def set_active(self, asset_representation):
        if asset_representation is None:
            self.active_index = -1
        else:
            i = 0  # Keep this to avoid unbound reference assignment
            for i, selected_asset_representation in enumerate(self.assets):
                if (
                    selected_asset_representation.full_library_path == asset_representation.full_library_path
                    and selected_asset_representation.id_type == asset_representation.id_type
                    and selected_asset_representation.name == asset_representation.name
                ):
                    self.active_index = i
                    break
            else:
                self.add_asset(asset_representation)
                self.active_index = i + 1

    @property
    def active_asset(self):
        return self.assets[self.active_index] if self.active_index >= 0 else None
