from enum import Enum
from pathlib import Path
from asset_browser_utilities.core.prop import StrProperty
from asset_browser_utilities.core.tool import copy_simple_property_group
from asset_browser_utilities.core.cache.tool import CacheMapping, get_from_cache
from asset_browser_utilities.core.filter.name import FilterName
from asset_browser_utilities.core.library.tool import get_blend_files_in_folder

import bpy
from bpy.types import PropertyGroup
from bpy.props import BoolProperty, EnumProperty, PointerProperty, CollectionProperty, StringProperty


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


class LibraryExportSettings(PropertyGroup, CacheMapping):
    source: EnumProperty(items=[(l_t.value,) * 3 for l_t in LibraryType])
    library_user_path: EnumProperty(
        name="User Library",
        items=lambda s, c: ((a_l.path, a_l.name, "") for a_l in c.preferences.filepaths.asset_libraries),
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
    files_prop: CollectionProperty(type=StrProperty)
    folder: StringProperty()
    filepath_prop: StringProperty()
    filepath_start: StringProperty()
    filter_files_names: PointerProperty(type=FilterName)

    @property
    def files(self):
        return [file.name for file in self.files_prop]

    @files.setter
    def files(self, value):
        self.files_prop.clear()
        for file in value:
            new = self.files_prop.add()
            new.name = file.name

    @property
    def filepath(self):
        return str(self.filepath_prop)

    @filepath.setter
    def filepath(self, value):
        self.filepath_prop = value
        folder = Path(self.filepath_prop)
        if folder.is_file():
            folder = folder.parent
        self.folder = str(folder)

    def init(self, remove_backup=False):
        self.remove_backup_allow = remove_backup
        self.remove_backup = remove_backup

    def draw(self, layout, context):
        if self.source == LibraryType.FileCurrent.value:
            return

        self.filter_files_names.draw(layout, name_override="Selected Files")
        if self.source == LibraryType.FolderExternal.value:
            layout.prop(self, "recursive", icon="FOLDER_REDIRECT")
        elif self.source == LibraryType.UserLibrary.value:
            box = layout.box()
            library_pg = get_from_cache(LibraryExportSettings)
            box.prop(library_pg, "library_user_path", icon="FOLDER_REDIRECT")
            box.label(text=f"Path : {library_pg.library_user_path}")
        if self.remove_backup_allow:
            layout.prop(self, "remove_backup", icon="TRASH")

    def copy_from(self, other):
        copy_simple_property_group(other, self)

    def get_blend_files(self):
        files = []
        if self.source == LibraryType.FileCurrent.value:
            files = [Path(bpy.data.filepath)]
        elif self.source == LibraryType.FileExternal.value:
            folder = Path(self.folder)
            files = [folder / filepath for filepath in self.files]
        elif self.source == LibraryType.FolderExternal.value:
            files = get_blend_files_in_folder(self.folder, recursive=self.recursive)
        else:  # User Library
            self.folder = Path(self.library_user_path)
            files = get_blend_files_in_folder(self.folder, recursive=True)
        files = [f for f in files if self.filter_files_names.filter(f.stem)]
        return files

    def __str__(self) -> str:
        ret = "Files Cache \n"
        ret += "Files : \n"
        ret += f"{self.files}\n"
        ret += "Filepath : \n"
        ret += self.filepath
        return ret
