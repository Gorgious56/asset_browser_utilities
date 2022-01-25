from enum import Enum
from pathlib import Path
from asset_browser_utilities.core.helper import copy_simple_property_group

import bpy
from bpy.types import PropertyGroup
from bpy.props import BoolProperty, StringProperty, EnumProperty


class LibraryType(Enum):
    FileCurrent = "file_current"
    FileExternal = "file_external"
    FolderExternal = "folder_external"
    UserLibrary = "user_library"

    @staticmethod
    def get(context):
        if hasattr(context, LibraryType.UserLibrary.value):
            return LibraryType.UserLibrary.value
        elif hasattr(context, LibraryType.FolderExternal.value):
            return LibraryType.FolderExternal.value
        elif hasattr(context, LibraryType.FileExternal.value):
            return LibraryType.FileExternal.value
        else:
            return LibraryType.FileCurrent.value


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

    def get_blend_files(self, blend_filepath=None):
        if self.library_type == LibraryType.FileCurrent.value:
            return [bpy.data.filepath]
        else:
            if self.library_type == LibraryType.FolderExternal.value:
                folder = Path(blend_filepath)
                if not folder.is_dir():
                    folder = folder.parent
            elif self.library_type == LibraryType.FileExternal.value:
                try:
                    iter(blend_filepath)
                except TypeError:
                    return [blend_filepath]
                else:
                    return blend_filepath
            else:
                folder = Path(self.library_path)
            if self.recursive:
                return [fp for fp in folder.glob("**/*.blend") if fp.is_file()]
            else:
                return [fp for fp in folder.glob("*.blend") if fp.is_file()]
