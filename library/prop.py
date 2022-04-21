from enum import Enum
from pathlib import Path
from asset_browser_utilities.core.helper import copy_simple_property_group
from asset_browser_utilities.library.tool import get_blend_files_in_folder

import bpy
from bpy.types import PropertyGroup
from bpy.props import BoolProperty, StringProperty, EnumProperty


class LibraryType(Enum):
    FileCurrent = "file_current"
    FileExternal = "file_external"
    FolderExternal = "folder_external"
    UserLibrary = "user_library"

    @staticmethod
    def get_library_type_from_context(context):
        if hasattr(context, LibraryType.UserLibrary.value):
            return LibraryType.UserLibrary.value
        elif hasattr(context, LibraryType.FolderExternal.value):
            return LibraryType.FolderExternal.value
        elif hasattr(context, LibraryType.FileExternal.value):
            return LibraryType.FileExternal.value
        else:
            return LibraryType.FileCurrent.value


class LibraryPG(PropertyGroup):
    library_type: EnumProperty(items=[(l_t.value,) * 3 for l_t in LibraryType])

    @staticmethod
    def set_library_type(context, library_type):
        context.screen.ABU_Library.library_type = library_type
    
    @staticmethod
    def get_library_type(context):
        return context.screen.ABU_Library.library_type


class LibraryExportSettings(PropertyGroup):
    library_type: StringProperty(name="Library Type")
    recursive: BoolProperty(
        default=True,
        name="Recursive",
        description="Operate on blend files located in sub folders recursively\nIf unchecked it will only treat files in this folder",
    )
    remove_backup: BoolProperty(
        name="Remove Backup",
        description="Check to automatically delete the creation of backup files when 'Save Versions' is enabled in the preferences\nThis will prevent duplicating files when they are overwritten\nWarning : Backup files ending in .blend1 will be deleted permantently",
        default=True,
    )
    remove_backup_allow: BoolProperty()
    library_path: EnumProperty(
        name="User Library",
        items=lambda s, c: ((a_l.path, a_l.name, "") for a_l in c.preferences.filepaths.asset_libraries),
    )

    def init(self, remove_backup=False):
        self.remove_backup_allow = remove_backup
        self.remove_backup = remove_backup

    def draw(self, layout):
        if self.library_type == LibraryType.FileCurrent.value:
            return
        elif self.library_type == LibraryType.FolderExternal.value:
            layout.prop(self, "recursive", icon="FOLDER_REDIRECT")
        elif self.library_type == LibraryType.UserLibrary.value:
            box = layout.box()
            box.prop(self, "library_path", icon="FOLDER_REDIRECT")
            box.label(text=f"Path : {self.library_path}")
        if self.remove_backup_allow:
            layout.prop(self, "remove_backup", icon="TRASH")

    def copy(self, other):
        copy_simple_property_group(other, self)

    def get_blend_files(self, folder=None, filepaths=None):
        if self.library_type == LibraryType.FileCurrent.value:
            return [bpy.data.filepath]
        elif self.library_type == LibraryType.FolderExternal.value:
            return get_blend_files_in_folder(folder, recursive=self.recursive)
        elif self.library_type == LibraryType.FileExternal.value:
            return [folder / filepath for filepath in filepaths]
        else:  # User Library
            folder = Path(self.library_path)
            return get_blend_files_in_folder(folder, recursive=True)

def register():
    bpy.types.Screen.ABU_Library = bpy.props.PointerProperty(type=LibraryPG)