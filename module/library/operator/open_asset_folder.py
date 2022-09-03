import webbrowser
import bpy
from asset_browser_utilities.module.asset.tool import get_selected_assets_folderpaths


class ABU_OT_open_asset_folder(bpy.types.Operator):
    bl_idname = "abu.open_asset_folder"
    bl_label = "Open Blend Folder(s)"
    bl_options = {"UNDO", "REGISTER"}

    def execute(self, context):
        # https://stackoverflow.com/a/54641180/7092409
        for path in get_selected_assets_folderpaths(context):
            webbrowser.open("file:///" + str(path))
        return {"FINISHED"}
