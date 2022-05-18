import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.file.path import get_folder_from_path
from asset_browser_utilities.preview.tool import create_image


class BatchExecuteOverride(BatchExecute):
    def __init__(self, operator, context):
        self.folder = get_folder_from_path(operator.filepath)
        super().__init__(operator, context)

    def do_on_asset(self, asset):
        asset_preview = asset.preview
        images = []
        if asset_preview is not None:
            img = create_image(asset.name, asset_preview.image_size[0], asset_preview.image_size[1])
            images.append(img)
            img.file_format = "PNG"
            for char in ("/", "\\", ":",  "|", '"', "!", "?", "<", ">", "*"):
                if char in img.name:
                    img.name = img.name.replace(char, "_")
            img.filepath = str(self.folder / (img.name + ".png"))
            img.pixels.foreach_set(asset_preview.image_pixels_float)
            img.save()
            print(f"Saved thumbnail from {asset.name} to {img.filepath}")
        bpy.data.batch_remove(images)
        super().do_on_asset(asset)


class OperatorProperties(PropertyGroup):
    pass


class ASSET_OT_previews_extract(Operator, BatchFolderOperator):
    bl_idname = "abu.previews_extract"
    bl_label = "Extract Previews to Disk"

    operator_settings: PointerProperty(type=OperatorProperties)
    logic_class = BatchExecuteOverride

    def invoke(self, context, event):
        self.filter_glob = ""
        return self._invoke(context, filter_assets=True, enforce_filebrowser=True)
