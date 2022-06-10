from pathlib import Path

import bpy.app.timers
from bpy.types import Operator
from bpy.props import PointerProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.library.prop import LibraryExportSettings

from asset_browser_utilities.core.library.tool import load_preview
from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.core.file.path import get_supported_images


class BatchExecuteOverride(BatchExecute):
    def __init__(self):
        folder = Path(get_from_cache(LibraryExportSettings).folder)
        self.images = list(get_supported_images(folder, recursive=True))
        self.images_names = [file.stem for file in self.images]
        super().__init__()

    def execute_one_file_and_the_next_when_finished(self):
        for asset in self.assets:
            if asset.name in self.images_names:
                image_filepath = str(self.images[self.images_names.index(asset.name)])
                load_preview(image_filepath, asset)
                Logger.display(f"Loaded custom preview from '{image_filepath}' for asset '{asset.name}'")
        self.execute_next_blend()


class ABU_OT_preview_import(Operator, BatchFolderOperator):
    bl_idname = "abu.preview_import"
    bl_label = "Load Previews From Disk"

    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True, enforce_filebrowser=True)
