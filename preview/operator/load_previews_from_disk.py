from pathlib import Path
import bpy
import bpy.app.timers
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, PointerProperty

from asset_browser_utilities.library.tool import load_preview
from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.file.path import get_supported_images


class BatchExecuteOverride(BatchExecute):
    def __init__(self, operator, context):
        folder = Path(operator.filepath)
        if folder.is_file():
            folder = folder.parent

        self.images = list(get_supported_images(folder, recursive=True))
        self.images_names = [file.stem for file in self.images]
        super().__init__(operator, context)

    def execute_one_file_and_the_next_when_finished(self):
        for asset in self.assets:
            if asset.name in self.images_names:
                load_preview(str(self.images[self.images_names.index(asset.name)]), asset)

        self.execute_next_blend()


class OperatorProperties(PropertyGroup):
    pass


class ASSET_OT_load_previews_from_disk(Operator, BatchFolderOperator):
    "Load Previews From Disk"
    bl_idname = "asset.load_previews_from_disk"
    bl_label = "Load Previews From Disk"

    operator_settings: PointerProperty(type=OperatorProperties)
    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True, enforce_filebrowser=True)
