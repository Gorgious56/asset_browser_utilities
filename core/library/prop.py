from enum import Enum
from pathlib import Path
from asset_browser_utilities.core.prop import StringPropertyCollection

from asset_browser_utilities.core.tool import copy_simple_property_group

from asset_browser_utilities.core.cache.tool import get_from_cache

from asset_browser_utilities.core.filter.date import FilterDate
from asset_browser_utilities.core.filter.name import FilterName

from asset_browser_utilities.core.library.tool import get_files_in_folder

import bpy
from bpy.types import PropertyGroup
from bpy.props import BoolProperty, EnumProperty, PointerProperty, CollectionProperty, StringProperty


class LibraryType(Enum):
    FileCurrent = "file_current"
    FileExternal = "file_external"
    FolderExternal = "folder_external"
    UserLibrary = "user_library"
    All = "ALL"

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

    @staticmethod
    def is_file_current(context):
        return LibraryType.get_library_type_from_context(context) == LibraryType.FileCurrent.value


class LibraryExportSettings(PropertyGroup):
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
        description="Check to automatically delete the creation of backup files when 'Save Versions' is enabled in the preferences\nThis will prevent duplicating files when they are overwritten\nWarning : Backup files ending in .blend1 will be deleted permanently",
        default=True,
    )
    remove_backup_allow: BoolProperty()
    files_prop: CollectionProperty(type=StringPropertyCollection)
    folder: StringProperty()
    filepath_start: StringProperty()
    filter_files_names: PointerProperty(type=FilterName)
    filter_date: PointerProperty(type=FilterDate)

    @property
    def files(self):
        return [file.name for file in self.files_prop]

    @files.setter
    def files(self, list_):
        self.files_prop.clear()
        for file in list_:
            self.add_file(file)

    def add_file(self, filepath):
        new = self.files_prop.add()
        new.name = str(filepath)

    @property
    def filepath(self):
        return self.files[0]

    def init(self, remove_backup=False):
        self.remove_backup_allow = remove_backup
        self.remove_backup = remove_backup
        self.filter_date.init()

    def draw_asset_library(self, layout):
        box = layout.box()
        box.prop(self, "library_user_path", icon="FOLDER_REDIRECT")
        box.label(text=f"Path : {self.library_user_path}")

    def draw(self, layout, context):
        self = get_from_cache(LibraryExportSettings)
        if self.source != LibraryType.FileCurrent.value:
            self.filter_files_names.draw(layout, name_override="Selected Files")
            self.filter_date.draw(layout)
            if self.source == LibraryType.FolderExternal.value:
                layout.prop(self, "recursive", icon="FOLDER_REDIRECT")
            elif self.source == LibraryType.UserLibrary.value:
                self.draw_asset_library(layout)
        if self.remove_backup_allow:
            layout.prop(self, "remove_backup", icon="TRASH")

    def copy_from(self, other):
        copy_simple_property_group(other, self)

    def filter_files_by_name(self, files):
        return [f for f in files if get_from_cache(LibraryExportSettings).filter_files_names.filter(f.stem)]

    def filter_files_by_date(self, files):
        # https://pynative.com/python-file-creation-modification-datetime/
        return [f for f in files if get_from_cache(LibraryExportSettings).filter_date.filter(f.stat().st_mtime)]

    def get_files(self, file_extension="blend"):
        self = get_from_cache(LibraryExportSettings)
        if self.source == LibraryType.FileCurrent.value:
            files = [Path(bpy.data.filepath)]
        elif self.source == LibraryType.FileExternal.value:
            files = [Path(f) for f in self.files]
        elif self.source == LibraryType.FolderExternal.value:
            files = get_files_in_folder(self.folder, recursive=self.recursive, extension=file_extension)
        else:  # User Library
            folder = Path(self.library_user_path)
            files = get_files_in_folder(folder, recursive=True, extension=file_extension)

        files = self.filter_files_by_name(files)
        files = self.filter_files_by_date(files)
        return files

    def __str__(self) -> str:
        ret = "Files Cache \n"
        ret += "Files : \n"
        ret += f"{self.files}\n"
        ret += "Filepath : \n"
        ret += self.filepath
        return ret
