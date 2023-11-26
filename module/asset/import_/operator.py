from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.library.tool import append_asset, get_directory_name

import bpy
from bpy.types import Operator, OperatorFileListElement, PropertyGroup
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty, CollectionProperty, PointerProperty

from asset_browser_utilities.core.operator.tool import BatchFolderOperator


class BatchImport:
    def __init__(self, *args, **kwargs):
        self.filepaths = []
        self.directories = []
        self.filenames = []
        super().__init__(*args, **kwargs)

    def execute_one_file_and_the_next_when_finished(self):
        if bpy.data.filepath != self.target_filepath:
            self.add_asset_paths()
            if not self.files:
                bpy.ops.wm.open_mainfile(filepath=str(self.target_filepath))
        if self.files:
            self.execute_next_file()
        else:
            bpy.app.timers.register(self.append_assets, first_interval=0.1)

    def add_asset_paths(self):
        for asset in self.assets:
            self.filepaths.append(str(self.file))
            self.directories.append(get_directory_name(asset))
            self.filenames.append(str(asset.name))
            Logger.display(f"Found '{self.filepaths[-1]}\\{self.directories[-1]}\\{self.filenames[-1]}'")

    def append_assets(self):
        for filepath, directory, filename in zip(self.filepaths, self.directories, self.filenames):
            append_asset(filepath, directory, filename)
            Logger.display(f"Import '{filepath}\\{directory}\\{filename}'")
        self.execute_next_file()


class OperatorProperties(PropertyGroup):
    target_filepath: StringProperty()


class ABU_OT_batch_import(Operator, ExportHelper):
    ui_library = LibraryType.FileExternal.value
    bl_idname = "abu.batch_import"
    bl_label = "Import Assets"
    bl_description: str = "Import Assets From External File or Library"

    filter_glob: StringProperty(
        default="*.blend",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    filename_ext = "*.blend"

    # https://docs.blender.org/api/current/bpy.types.OperatorFileListElement.html
    files: CollectionProperty(
        type=OperatorFileListElement,
        options={"HIDDEN", "SKIP_SAVE"},
    )

    operator_settings: PointerProperty(type=OperatorProperties)
    logic_class = BatchImport

    def invoke(self, context, event):
        self.filepath = ""
        self.operator_settings.target_filepath = bpy.data.filepath
        return self._invoke(context, remove_backup=False, filter_assets=True)
