from pathlib import Path

from bpy.types import Operator, PropertyGroup
from bpy.props import BoolProperty, PointerProperty, StringProperty, IntProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.library.prop import LibraryExportSettings

from asset_browser_utilities.core.library.tool import load_preview
from asset_browser_utilities.core.file.path import get_supported_images
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps


class PreviewImportOperatorProperties(PropertyGroup, BaseOperatorProps):
    look_only_in_folder_with_name: StringProperty(
        name="Image Folder Name",
        description="Look only in subfolders with this name. \nLeave empty to not filter folders.",
        default="",
    )
    exact_match: BoolProperty(
        name="Match Name Exactly", default=True, description="Match Image and Asset names exactly"
    )
    load_if_name_contains_image_name: BoolProperty(
        name="Strip Suffix",
        description="Load preview if image name is contained in the first letters of the asset name\n\
        (if image file name is 'asset.jpg', it will be loaded to an asset named 'asset.001'",
        default=False,
    )
    match_sequence: IntProperty(
        name="Match Character Sequence",
        description="Match Image and Asset Name if there is a sequence of characters of at least this length in common\n\
        (eg. image name = 'def.jpg' and asset name = 'abcde', if sequence = 2, it will match, if sequence = 3, it won't)",
        default=0,
        min=0,
        max=256,
    )

    def draw(self, layout, context=None):
        layout.prop(self, "look_only_in_folder_with_name", icon="FILTER")
        layout.prop(self, "exact_match")
        if not self.exact_match:
            layout.prop(self, "load_if_name_contains_image_name", icon="OUTLINER_OB_FONT")
            layout.prop(self, "match_sequence")

    def check_sequence(self, string1, string2, sequence_length):
        for i in range(len(string1) - sequence_length + 1):
            sequence = string1[i : i + sequence_length]
            if sequence in string2:
                return True
        return False

    def run_in_file(self, attributes=None):
        folder = Path(get_from_cache(LibraryExportSettings).folder)
        images = list(get_supported_images(folder, recursive=True))
        look_only_in_folder_with_name = self.look_only_in_folder_with_name
        if look_only_in_folder_with_name != "":
            images = [img for img in images if img.parent.name == look_only_in_folder_with_name]
        images_names = [file.stem for file in images]
        should_save = False
        for asset in self.get_assets():
            asset_name = asset.name
            if asset_name in images_names:
                filepath = str(images[images_names.index(asset_name)])
                self.load_preview(asset, filepath)
                should_save = True
            elif not self.exact_match:
                if self.load_if_name_contains_image_name:
                    for image_name in images_names:
                        if asset_name.startswith(image_name):
                            filepath = str(images[images_names.index(image_name)])
                            self.load_preview(asset, filepath)
                            should_save = True
                            break
                elif self.match_sequence > 0:
                    for image_name in images_names:
                        if self.check_sequence(image_name, asset_name, sequence_length=self.match_sequence):
                            filepath = str(images[images_names.index(image_name)])
                            self.load_preview(asset, filepath)
                            should_save = True
                            break
        return should_save

    def load_preview(self, asset, image_filepath):
        load_preview(image_filepath, asset)


class ABU_OT_preview_import(Operator, BatchFolderOperator):
    bl_idname = "abu.preview_import"
    bl_label = "Load Previews From Disk"

    operator_settings: PointerProperty(type=PreviewImportOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True, enforce_filebrowser=True)
