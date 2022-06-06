import bpy
from bpy.types import PropertyGroup
from bpy.props import StringProperty, CollectionProperty


class SelectedAssetFile(PropertyGroup):
    container: StringProperty()
    name: StringProperty()


class SelectedAssetFiles(PropertyGroup):
    files_prop: CollectionProperty(type=SelectedAssetFile)
    
    def init(self):
        self.files_prop.clear()

    def add(self, container, _id):
        if _id is None:
            return
        new = self.files_prop.add()
        new.container = container.lower() + "s"
        new.name = _id.name
        
    @property
    def assets(self):
        for file in self.files_prop:
            yield (getattr(bpy.data, file.container).get(file.name))
