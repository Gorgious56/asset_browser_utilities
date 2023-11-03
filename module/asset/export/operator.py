from pathlib import Path
import os
from asset_browser_utilities.core.cache.tool import get_current_operator_properties, get_from_cache
from asset_browser_utilities.core.file.save import save_if_possible_and_necessary
from asset_browser_utilities.core.filter.main import AssetFilterSettings
from asset_browser_utilities.core.library.prop import LibraryExportSettings, LibraryType

import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, PointerProperty, BoolProperty

from asset_browser_utilities.core.file.path import get_folder_from_path
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.library.tool import get_directory_name
from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.core.console.builder import CommandBuilder


class AssetExportOperatorProperties(PropertyGroup):
    individual_files: BoolProperty(
        name="Place Assets in Individual Files",
        description="If this is ON, each asset will be exported to an individual file in the target directory.\
\nEach asset will be placed in a blend file named after itself\
\nBeware of name collisions",
    )
    type_folders: BoolProperty(
        name="Place Assets in Type Folders",
        default=True,
    )
    overwrite: BoolProperty(
        name="Overwrite Assets",
        description="Check to overwrite objects if an object with the same name already exists in target file",
        default=True,
    )

    def draw(self, layout, context=None):
        layout.prop(self, "individual_files", icon="NEWFOLDER")
        type_folders_row = layout.row()
        type_folders_row.prop(self, "type_folders", icon="OUTLINER")
        type_folders_row.active = self.individual_files
        layout.prop(self, "overwrite", icon="ASSET_MANAGER")


class ABU_OT_asset_export(Operator, BatchFolderOperator):
    ui_library = LibraryType.FileCurrent.value
    bl_idname = "abu.asset_export"
    bl_label = "Export Assets"
    bl_description: str = "Export Assets To External File(s)"

    operator_settings: PointerProperty(type=AssetExportOperatorProperties)
    logic_class = BatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True, enforce_filebrowser=True)

    def execute(self, context):
        self.write_filepath_to_cache()
        save_if_possible_and_necessary()
        self.populate_asset_and_asset_names()
        if len(self.asset_names) > 0:
            self.execute_in_new_blender_instance()
        else:
            Logger.display("No asset to export")
        return {"FINISHED"}

    def execute_in_new_blender_instance(self):
        current_operator_properties = get_current_operator_properties()
        caller = CommandBuilder(Path(os.path.realpath(__file__)))
        for name in self.asset_names:
            caller.add_arg_value("asset_names", name)
        for _type in self.asset_types:
            caller.add_arg_value("asset_types", _type)
        caller.add_arg_value("source_file", bpy.data.filepath)
        caller.add_arg_value("filepath", self.filepath)
        caller.add_arg_value("folder", str(get_folder_from_path(self.filepath)))
        caller.add_arg_value("remove_backup", get_from_cache(LibraryExportSettings).remove_backup)
        caller.add_arg_value("overwrite", current_operator_properties.overwrite)
        caller.add_arg_value("individual_files", current_operator_properties.individual_files)
        caller.add_arg_value("type_folders", current_operator_properties.type_folders)
        caller.call()

    def populate_asset_and_asset_names(self):
        assets = get_from_cache(AssetFilterSettings).get_objects_that_satisfy_filters()
        self.asset_names = [a.name for a in assets]
        self.asset_types = [get_directory_name(a) for a in assets]
