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

    def draw(self, layout):        
        if not self.this_file_only:
            layout.prop(self, "recursive", icon="FOLDER_REDIRECT")
    
    def copy(self, other):
        self.this_file_only = other.this_file_only
        self.recursive = other.recursive
