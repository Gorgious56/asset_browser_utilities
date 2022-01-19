def is_library(context):
    return hasattr(context, "abu_library")


def is_library_user(context):
    return hasattr(context, "abu_library_user")


def set_layout_library(layout):
    # Doc : https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.context_pointer_set
    # Howto : https://blender.stackexchange.com/questions/45845/how-to-create-submenus-with-dynamic-content
    layout.context_pointer_set("abu_library", None)


def set_layout_library_user(layout):
    layout.context_pointer_set("abu_library_user", None)
