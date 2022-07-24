from asset_browser_utilities.core.filter.main import AssetFilterSettings
from bpy.types import PropertyGroup
from bpy.props import StringProperty


class CurrentOperatorProperty(PropertyGroup):
    class_name: StringProperty()


class ObjectFilteredOperation:
    @staticmethod
    def poll():
        return AssetFilterSettings.are_objects_filtered()


class ObjectMeshFilteredOperation:
    @staticmethod
    def poll():
        return AssetFilterSettings.are_mesh_objects_filtered()
