from asset_browser_utilities.library.helper import append_asset, get_blend_library_name

import bpy
from bpy.types import Operator, OperatorFileListElement, PropertyGroup
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty, CollectionProperty, PointerProperty

from asset_browser_utilities.library.execute import BatchExecute
from asset_browser_utilities.library.operator import BatchFolderOperator


class BatchImport(BatchExecute):
    def __init__(self, *args, **kwargs):
        self.filepaths = []
        self.directories = []
        self.filenames = []
        super().__init__(*args, **kwargs)

    def execute_one_file_and_the_next_when_finished(self):
        if bpy.data.filepath != self.target_filepath:
            self.add_asset_paths()
            if not self.blends:
                bpy.ops.wm.open_mainfile(filepath=str(self.target_filepath))
        if self.blends:
            self.execute_next_blend()
        else:
            bpy.app.timers.register(self.append_assets, first_interval=0.1)

    def add_asset_paths(self):
        for asset in self.assets:
            self.filepaths.append(str(self.blend))
            self.directories.append(str(get_blend_library_name(asset)))
            self.filenames.append(str(asset.name))

    def append_assets(self):
        for filepath, directory, filename in zip(self.filepaths, self.directories, self.filenames):
            append_asset(filepath, directory, filename)
        self.execute_next_blend()


class OperatorProperties(PropertyGroup):
    target_filepath: StringProperty()


class ASSET_OT_batch_import(Operator, ExportHelper, BatchFolderOperator):
    "Import Assets From External File or Library"
    bl_idname = "asset.batch_import"
    bl_label = "Import Assets"

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
