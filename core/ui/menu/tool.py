# Doc : https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.context_pointer_set
# Howto : https://blender.stackexchange.com/questions/45845/how-to-create-submenus-with-dynamic-content

from asset_browser_utilities.core.library.prop import LibraryType


def set_layout_library_file_external(layout):
    layout.context_pointer_set(LibraryType.FileExternal.value, None)


def set_layout_library_folder(layout):
    layout.context_pointer_set(LibraryType.FolderExternal.value, None)


def set_layout_library_user(layout):
    layout.context_pointer_set(LibraryType.UserLibrary.value, None)


def is_library_file_current(context):
    return (
        not hasattr(context, LibraryType.FileExternal.value)
        and not hasattr(context, LibraryType.FolderExternal.value)
        and not hasattr(context, LibraryType.UserLibrary.value)
    )


def is_library_file_external(context):
    return hasattr(context, LibraryType.FileExternal.value)


def is_library_folder(context):
    return hasattr(context, LibraryType.FolderExternal.value) and not is_library_file_external(context)


def is_library_user(context):
    return hasattr(context, LibraryType.UserLibrary.value) and not is_library_folder(context) and not is_library_file_external(context)
