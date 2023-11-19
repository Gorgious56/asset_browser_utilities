import bpy
from bpy.types import PropertyGroup
from bpy.props import StringProperty, CollectionProperty, PointerProperty

from asset_browser_utilities.core.library.tool import get_blend_data_name


class SelectedAssetFile(PropertyGroup):
    container: StringProperty()
    name: StringProperty()


class SelectedAssetFiles(PropertyGroup):
    active_asset_prop: PointerProperty(type=SelectedAssetFile)
    files_prop: CollectionProperty(type=SelectedAssetFile)

    def init(self):
        self.files_prop.clear()

    def add(self, _id):
        if _id is None:
            return
        new = self.files_prop.add()
        new.container = get_blend_data_name(_id)
        new.name = _id.name

    def set_active(self, _id):
        if _id is None:
            return
        self.active_asset_prop.container = get_blend_data_name(_id)
        self.active_asset_prop.name = _id.name

    @property
    def assets(self):
        for file in self.files_prop:
            yield (getattr(bpy.data, file.container).get(file.name))

    @property
    def active_asset(self):
        return getattr(bpy.data, self.active_asset_prop.container).get(self.active_asset_prop.name)
