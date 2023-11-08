import webbrowser
import bpy
from asset_browser_utilities.module.asset.tool import get_selected_linked_objects_in_outliner


class ABU_OT_open_asset_folder(bpy.types.Operator):
    bl_idname = "abu.open_linked_object_blend_file"
    bl_label = "Open Linked Object's Blend File"
    bl_options = {"UNDO", "REGISTER"}
    
    @classmethod
    def poll(cls, context):
        return len(list(get_selected_linked_objects_in_outliner(context))) > 0

    def execute(self, context):
        for path in get_selected_linked_objects_in_outliner(context):
            webbrowser.open("file:///" + str(path))
        return {"FINISHED"}
