# Doc : https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.context_pointer_set
# Howto : https://blender.stackexchange.com/questions/45845/how-to-create-submenus-with-dynamic-content

from asset_browser_utilities.library.prop import LibraryType


def set_layout_file_external(layout):
    layout.context_pointer_set(LibraryType.FileExternal.value, None)


def set_layout_folder_external(layout):
    layout.context_pointer_set(LibraryType.FolderExternal.value, None)


def set_layout_library_user(layout):
    layout.context_pointer_set(LibraryType.UserLibrary.value, None)


def is_current_file(context):
    return (
        not hasattr(context, LibraryType.FileExternal.value)
        and not hasattr(context, LibraryType.FolderExternal.value)
        and not hasattr(context, LibraryType.UserLibrary.value)
    )
