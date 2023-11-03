import bpy
from pathlib import Path
from asset_browser_utilities.core.library.tool import get_blend_data_name_from_directory
from asset_browser_utilities.core.log.logger import Logger


class ABU_OT_open_asset_folder(bpy.types.Operator):
    bl_idname = "abu.linked_users"
    bl_label = "Show Linked Users"
    bl_options = {"UNDO", "REGISTER"}

    def execute(self, context):
        if context is None:
            context = bpy.context
        current_library_name = context.area.spaces.active.params.asset_library_ref

        if current_library_name == "LOCAL":  # Current file
            pass
        else:
            library_path = Path(context.preferences.filepaths.asset_libraries.get(current_library_name).path)
            blend_files = [fp for fp in library_path.glob("**/*.blend") if fp.is_file()]
            print(f"Checking the content of library '{library_path}' :")
            for asset_file in context.selected_asset_files:
                blend_data_name = get_blend_data_name_from_directory(asset_file.id_type)
                users = 0
                for blend_file in blend_files:
                    with bpy.data.libraries.load(str(blend_file), link=True) as (file_contents, _):
                        container = list(getattr(file_contents, blend_data_name))
                        print(container)
                        users += container.count(asset_file.name)
                        print(users)
                Logger.display(f"Asset {asset_file.name} has {users} users, including itself")

        return {"FINISHED"}
