# Doc : https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.context_pointer_set
# Howto : https://blender.stackexchange.com/questions/45845/how-to-create-submenus-with-dynamic-content

from asset_browser_utilities.core.library.prop import LibraryType


def set_layout_library_file_external(layout):
    layout.context_pointer_set(LibraryType.FileExternal.value, None)


def set_layout_library_folder(layout):
    layout.context_pointer_set(LibraryType.FolderExternal.value, None)


def set_layout_library_user(layout):
    layout.context_pointer_set(LibraryType.UserLibrary.value, None)
