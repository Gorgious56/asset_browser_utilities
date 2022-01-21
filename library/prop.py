from enum import Enum
from pathlib import Path
from asset_browser_utilities.core.ui.menu.helper import is_library, is_library_user

import bpy
from bpy.types import PropertyGroup
from bpy.props import BoolProperty, IntProperty, EnumProperty


class LibraryType(Enum):
    FileCurrent = 0
    FileOrFolder = 1
    User = 2

    @staticmethod
    def get(context):
        if is_library(context):
            if is_library_user(context):
                return LibraryType.User.value
            return LibraryType.FileOrFolder.value
        return LibraryType.FileCurrent.value


class LibraryExportSettings(PropertyGroup):
    this_file_only: IntProperty(
        default=False,
        name="Act only on this file",
    )
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
        if self.this_file_only == LibraryType.FileCurrent.value:
            return
        elif self.this_file_only == LibraryType.FileOrFolder.value:
            layout.prop(self, "recursive", icon="FOLDER_REDIRECT")
        elif self.this_file_only == LibraryType.User.value:
            box = layout.box()
            box.prop(self, "library_path", icon="FOLDER_REDIRECT")
            box.label(text=f"Path : {self.library_path}")
        if self.remove_backup_allow:
            layout.prop(self, "remove_backup", icon="TRASH")

    def copy(self, other):
        self.this_file_only = other.this_file_only
        self.recursive = other.recursive

    def get_blend_files(self, blend_filepath=None):
        if self.this_file_only == LibraryType.FileCurrent.value:
            return [bpy.data.filepath]
        else:
            if self.this_file_only == LibraryType.FileOrFolder.value:
                folder = Path(blend_filepath)
                if not folder.is_dir():
                    folder = folder.parent
            else:
                folder = Path(self.library_path)
            if self.recursive:
                return [fp for fp in folder.glob("**/*.blend") if fp.is_file()]
            else:
                return [fp for fp in folder.glob("*.blend") if fp.is_file()]