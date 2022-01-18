import os
from pathlib import Path
from asset_browser_utilities.filter.main import AssetFilterSettings

import bpy
from bpy.types import Operator, OperatorFileListElement
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty, PointerProperty, CollectionProperty

from asset_browser_utilities.console.builder import CommandBuilder
from asset_browser_utilities.core.operator.helper import FilterLibraryOperator
from asset_browser_utilities.file.path import (
    is_this_current_file,
)

from asset_browser_utilities.file.save import save_if_possible_and_necessary
from asset_browser_utilities.library.helper import get_all_assets_in_file, generate_asset_preview
from asset_browser_utilities.file.path import get_supported_images
from asset_browser_utilities.core.preferences.helper import get_from_cache, write_to_cache
from asset_browser_utilities.asset.import_.prop import CacheAssetPaths


class ASSET_OT_batch_import(Operator, ExportHelper, FilterLibraryOperator):
    "Import Assets From External File or Library"
    bl_idname = "asset.batch_import"
    bl_label = "Import Assets"

    filter_glob: StringProperty(
        default="*.blend",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    # https://docs.blender.org/api/current/bpy.types.OperatorFileListElement.html
    files: CollectionProperty(
        type=OperatorFileListElement,
        options={"HIDDEN", "SKIP_SAVE"},
    )

    def invoke(self, context, event):
        self.filepath = ""
        self.library_settings.this_file_only = False
        return self._invoke(context, remove_backup=False, filter_assets=True)

    def execute(self, context):
        if self.is_only_folder_selected():
            self.load_from_folder(context)
        else:
            self.load_from_selected_files()
        return {"FINISHED"}

    def load_from_folder(self, context):
        folder = Path(self.filepath)
        blends = self.library_settings.get_blend_files(self.filepath)
        prop = get_from_cache(CacheAssetPaths)
        prop.items.clear()

        write_to_cache(self.asset_filter_settings, context)

        asset_filter_settings = get_from_cache(AssetFilterSettings)
        print(asset_filter_settings.filter_types.items)
        bpy.ops.wm.save_userpref()
        caller = CommandBuilder(Path(os.path.realpath(__file__)))
        for blend_filepath in blends:
            caller.add_arg_value("blends", str(blend_filepath))
        caller.call()
        print("done !!! qsd!fs!qdqs")

        #         bpy.ops.wm.append(
        #     filepath=str(self.source_file / self.current_asset_type / self.current_asset_name),
        #     directory=str(self.source_file / self.current_asset_type),
        #     filename=self.current_asset_name,
        # )
        # for extension in get_supported_images(folder, self.library_settings.recursive):
        #     files.extend(extension)
        # files_basenames_without_ext = [os.path.splitext(os.path.basename(file))[0] for file in files]
        # for asset in self.assets:
        #     asset_name = asset.name
        #     try:
        #         index = files_basenames_without_ext.index(asset_name)
        #         generate_asset_preview(str(files[index]), asset)
        #     except ValueError:
        #         pass

    def load_from_selected_files(self):
        folder = Path(self.filepath).parent
        files = [f.name for f in self.files]
        files_basenames_without_ext = [os.path.splitext(file)[0] for file in files]
        for asset in self.assets:
            asset_name = asset.name
            try:
                index = files_basenames_without_ext.index(asset_name)
                generate_asset_preview(str(folder / files[index]), asset)
            except ValueError:
                pass

    def load_from_file(self, file):
        pass

    def is_only_folder_selected(self):
        return self.files[0].name == ""

    def draw(self, context):
        layout = self.layout
        self.library_settings.draw(layout)
        self.asset_filter_settings.draw(layout)
        prop = get_from_cache(CacheAssetPaths)
        prop.draw(layout)
