from bpy.types import PropertyGroup
from bpy.props import BoolProperty, StringProperty, CollectionProperty


class CacheAssetPath(PropertyGroup):
    filename: StringProperty()
    directory: StringProperty()
    filepath: StringProperty()


# class CacheAssetPaths(PropertyGroup):
#     items: CollectionProperty(type=CacheAssetPath)

#     def draw(self, layout):
#         # Used for debugging purpose
#         for item in self.items:
#             for prop_name in item.__annotations__:
#                 layout.prop(item, prop_name)


class ExportProperties(PropertyGroup):
    individual_files: BoolProperty(
        name="Place Assets in Individual Files",
        description="If this is ON, each asset will be exported to an individual file in the target directory",
    )
    overwrite: BoolProperty(
        name="Overwrite Assets",
        description="Check to overwrite objects if an object with the same name already exists in target file",
        default=True,
    )
    open_in_new_blender_instance: BoolProperty(
        default=True,
        name="Open New Blender Instance",
        description="If checked, the file where the assets will be exported will be opened in a new blender instance",
    )

    def draw(self, layout):
        layout.prop(self, "open_in_new_blender_instance", icon="WINDOW")
        layout.prop(self, "individual_files", icon="NEWFOLDER")
        layout.prop(self, "overwrite", icon="ASSET_MANAGER")
