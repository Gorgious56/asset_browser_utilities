import bpy


def draw(self, context):
    self.layout.operator("abu.asset_libraries_sort")


def register():
    bpy.types.USERPREF_PT_file_paths_asset_libraries.prepend(draw)


def unregister():
    bpy.types.USERPREF_PT_file_paths_asset_libraries.remove(draw)
