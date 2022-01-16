from bpy.types import PropertyGroup
from bpy.props import BoolProperty


class LibraryExportSettings(PropertyGroup):
    this_file_only: BoolProperty(
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

    def init(self, remove_backup=False):
        self.remove_backup_allow = remove_backup
        self.remove_backup = remove_backup

    def draw(self, layout):
        if not self.this_file_only:
            layout.prop(self, "recursive", icon="FOLDER_REDIRECT")
            if self.remove_backup_allow:
                layout.prop(self, "remove_backup", icon="TRASH")

    def copy(self, other):
        self.this_file_only = other.this_file_only
        self.recursive = other.recursive
