import bpy
from uuid import uuid4


class ABU_OT_asset_libraries_sort(bpy.types.Operator):
    bl_idname = "abu.asset_libraries_sort"
    bl_label = "Sort By Name"
    bl_options = {"UNDO", "REGISTER"}

    def execute(self, context):
        asset_libraries = context.preferences.filepaths.asset_libraries
        asset_libraries_sorted = asset_libraries[:]
        asset_libraries_sorted.sort(key=lambda al: al.name)
        names = [a_l.name for a_l in asset_libraries_sorted]
        paths = [a_l.path for a_l in asset_libraries_sorted]

        for asset_library in asset_libraries:
            asset_library.name += str(uuid4())  # Two libs can't share the same name

        for i, (name, path) in enumerate(zip(names, paths)):
            asset_libraries[i].name = name
            asset_libraries[i].path = path
        return {"FINISHED"}
