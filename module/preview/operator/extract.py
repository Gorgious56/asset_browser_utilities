from pathlib import Path
from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.library.prop import LibraryExportSettings
import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.core.file.path import get_folder_from_path
from asset_browser_utilities.module.preview.tool import create_image


class BatchExecuteOverride(BatchExecute):
    def do_on_asset(self, asset):
        folder = Path(get_from_cache(LibraryExportSettings).folder)
        asset_preview = asset.preview
        images = []
        if asset_preview is not None:
            img = create_image(asset.name, asset_preview.image_size[0], asset_preview.image_size[1])
            images.append(img)
            img.file_format = "PNG"
            for char in ("/", "\\", ":",  "|", '"', "!", "?", "<", ">", "*"):
                if char in img.name:
                    img.name = img.name.replace(char, "_")
            img.filepath = str(folder / (img.name + ".png"))
            try:
                img.pixels.foreach_set(asset_preview.image_pixels_float)
            except TypeError:
                Logger.display(f"Could not save thumbnail from '{asset.name}'")
            else:
                img.save()
                Logger.display(f"Saved thumbnail from '{asset.name}' to '{img.filepath}'")
        bpy.data.batch_remove(images)
        super().do_on_asset(asset)


class ABU_OT_preview_extract(Operator, BatchFolderOperator):
    bl_idname = "abu.preview_extract"
    bl_label = "Extract Previews to Disk"

    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        self.filter_glob = ""
        return self._invoke(context, filter_assets=True, enforce_filebrowser=True)
