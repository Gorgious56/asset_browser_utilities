from pathlib import Path
import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import BoolProperty, PointerProperty

from asset_browser_utilities.core.cache.tool import get_current_operator_properties, get_from_cache
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.library.prop import LibraryExportSettings, LibraryType
from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator

from asset_browser_utilities.module.preview.tool import create_image


class PreviewExtractBatchExecute(BatchExecute):
    def do_on_asset(self, asset):

        op_props = get_current_operator_properties()
        if op_props.place_at_root:
            folder = Path(get_from_cache(LibraryExportSettings).folder)
        else:
            folder = Path(bpy.data.filepath).parent
        asset_preview = asset.preview
        images = []
        if asset_preview is not None:
            img = create_image(asset.name, asset_preview.image_size[0], asset_preview.image_size[1])
            images.append(img)
            img.file_format = "PNG"
            for char in ("/", "\\", ":", "|", '"', "!", "?", "<", ">", "*"):
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


class PreviewExtractOperatorProperties(PropertyGroup):
    place_at_root: BoolProperty(
        name="Place at Root",
        description="Toggle ON to save the thumbnails at the root of the library.\nOtherwise each thumbnail will be placed alongside each blend file",
        default=False,
    )

    def draw(self, layout):
        if get_from_cache(LibraryExportSettings).source != LibraryType.FileCurrent.value:
            layout.prop(self, "place_at_root", icon="FILEBROWSER")


class ABU_OT_preview_extract(Operator, BatchFolderOperator):
    bl_idname = "abu.preview_extract"
    bl_label = "Extract Previews to Disk"

    operator_settings: PointerProperty(type=PreviewExtractOperatorProperties)
    logic_class = PreviewExtractBatchExecute

    def invoke(self, context, event):
        self.filter_glob = ""
        return self._invoke(context, filter_assets=True, enforce_filebrowser=True)
