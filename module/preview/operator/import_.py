from pathlib import Path

from bpy.types import Operator, PropertyGroup
from bpy.props import BoolProperty, PointerProperty, StringProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.cache.tool import get_current_operator_properties, get_from_cache
from asset_browser_utilities.core.library.prop import LibraryExportSettings

from asset_browser_utilities.core.library.tool import load_preview
from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.core.file.path import get_supported_images


class PreviewImportBatchExecute(BatchExecute):
    def __init__(self):
        folder = Path(get_from_cache(LibraryExportSettings).folder)
        self.images = list(get_supported_images(folder, recursive=True))
        look_only_in_folder_with_name = get_current_operator_properties().look_only_in_folder_with_name
        if look_only_in_folder_with_name != "":
            self.images = [img for img in self.images if img.parent.name == look_only_in_folder_with_name]
        self.images_names = [file.stem for file in self.images]
        super().__init__()

    def execute_one_file_and_the_next_when_finished(self):
        op_props = get_current_operator_properties()
        imported_preview = False
        for asset in self.assets:
            asset_name = asset.name
            if asset_name in self.images_names:
                self.load_preview(asset, asset_name)
                imported_preview = True
            elif op_props.load_if_name_contains_image_name:
                for image_name in self.images_names:
                    if asset_name.startswith(image_name):
                        self.load_preview(asset, image_name)
                        imported_preview = True
                        break
        if imported_preview:
            self.save_file()
        self.execute_next_blend()

    def load_preview(self, asset, image_name):
        image_filepath = str(self.images[self.images_names.index(image_name)])
        load_preview(image_filepath, asset)


class PreviewImportOperatorProperties(PropertyGroup):
    load_if_name_contains_image_name: BoolProperty(
        name="Strip Suffix",
        description="Load preview if image name is contained in the first letters of the asset name\n\
        (if image file name is 'asset.jpg', it will be loaded to an asset named 'asset.001'",
        default=False,
    )
    look_only_in_folder_with_name: StringProperty(
        name="Image Folder Name",
        description="Look only in subfolders with this name. \nLeave empty to not filter folders.",
        default="",
    )

    def draw(self, layout):
        layout.prop(self, "load_if_name_contains_image_name", icon="OUTLINER_OB_FONT")
        layout.prop(self, "look_only_in_folder_with_name", icon="FILTER")


class ABU_OT_preview_import(Operator, BatchFolderOperator):
    bl_idname = "abu.preview_import"
    bl_label = "Load Previews From Disk"

    logic_class = PreviewImportBatchExecute
    operator_settings: PointerProperty(type=PreviewImportOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True, enforce_filebrowser=True)
