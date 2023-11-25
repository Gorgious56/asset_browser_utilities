import bpy


def unregister():
    del bpy.types.WindowManager.abu_progress_factor


def register():
    bpy.types.WindowManager.abu_progress_factor = bpy.props.FloatProperty(default=-1)
