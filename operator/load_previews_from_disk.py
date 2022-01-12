import os.path
from pathlib import Path
import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, OperatorFileListElement
from bpy.props import StringProperty, CollectionProperty, PointerProperty

from asset_browser_utilities.helper.library import get_all_assets_in_file, generate_asset_preview
from asset_browser_utilities.prop.path import LibraryExportSettings
from asset_browser_utilities.helper.path import get_supported_images


class ASSET_OT_load_previews_from_disk(Operator, ImportHelper):
    bl_idname = "asset.load_previews_from_disk"
    bl_label = "Load Previews From Disk"

    filter_glob: StringProperty(
        default="*" + ";*".join(bpy.path.extensions_image),
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    # https://docs.blender.org/api/current/bpy.types.OperatorFileListElement.html
    files: CollectionProperty(
            type=OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
        )
    library_export_settings: PointerProperty(type=LibraryExportSettings)

    def invoke(self, context, event):
        self.filepath = ""
        self.library_export_settings.this_file_only = False
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        self.assets = get_all_assets_in_file()
        if self.is_only_folder_selected():
            self.load_from_folder()
        else:
            self.load_from_selected_files()
        return {"FINISHED"}
    
    def load_from_folder(self):        
        folder = Path(self.filepath)
        files = []
        for extension in get_supported_images(folder, self.library_export_settings.recursive):
            files.extend(extension)
        files_basenames_without_ext = [os.path.splitext(os.path.basename(file))[0] for file in files]
        for asset in self.assets:
            asset_name = asset.name
            try:
                index = files_basenames_without_ext.index(asset_name)
                generate_asset_preview(str(files[index]), asset)
            except ValueError:
                pass

    def load_from_selected_files(self):
        folder = Path(self.filepath).parent
        files = [f.name for f in self.files]
        files_basenames_without_ext = [os.path.splitext(file)[0] for file in files]
        for asset in self.assets:
            asset_name = asset.name
            try:
                index = files_basenames_without_ext.index(asset_name)                    
                generate_asset_preview(os.path.join(folder, files[index]), asset)
            except ValueError:
                pass

    def is_only_folder_selected(self):
        return self.files[0].name == ""

    def draw(self, context):
        layout = self.layout
        self.library_export_settings.draw(layout)
