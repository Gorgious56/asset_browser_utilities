from pathlib import Path

import bpy
from bpy.types import Operator, OperatorFileListElement
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty, CollectionProperty

from asset_browser_utilities.core.operator.helper import FilterLibraryOperator

from asset_browser_utilities.file.save import save_if_possible_and_necessary
from asset_browser_utilities.core.preferences.helper import get_from_cache, write_to_cache
from asset_browser_utilities.asset.import_.prop import CacheAssetPaths
from asset_browser_utilities.library.prop import LibraryType

from .helper import BatchHelper


class ASSET_OT_batch_import(Operator, ExportHelper, FilterLibraryOperator):
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

    def invoke(self, context, event):
        self.filepath = ""
        self.library_settings.library_type = LibraryType.FileCurrent.value
        return self._invoke(context, remove_backup=False, filter_assets=True)

    def execute(self, context):
        save_if_possible_and_necessary()
        write_to_cache(self.asset_filter_settings, context)
        if self.is_only_folder_selected():
            self.load_from_folder(context)
        else:
            self.load_from_selected_files()
        return {"FINISHED"}

    def load_from_folder(self, context):
        blends = self.library_settings.get_blend_files(self.filepath)
        self.execute_in_this_instance(blends)

    def load_from_selected_files(self):
        folder = Path(self.filepath).parent
        blends = [folder / f.name for f in self.files]
        self.execute_in_this_instance(blends)

    def execute_in_this_instance(self, blends):
        BatchHelper(target_filepath=bpy.data.filepath, blend_filepaths=blends, from_command_line=False).execute()

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
