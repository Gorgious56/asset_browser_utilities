from pathlib import Path
import os

import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, PointerProperty, BoolProperty

from asset_browser_utilities.file.path import get_folder_from_path
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.library.tool import get_blend_library_name
from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.core.console.builder import CommandBuilder


class OperatorProperties(PropertyGroup):
    individual_files: BoolProperty(
        name="Place Assets in Individual Files",
        description="If this is ON, each asset will be exported to an individual file in the target directory",
    )
    overwrite: BoolProperty(
        name="Overwrite Assets",
        description="Check to overwrite objects if an object with the same name already exists in target file",
        default=True,
    )

    def draw(self, layout):
        layout.prop(self, "individual_files", icon="NEWFOLDER")
        layout.prop(self, "overwrite", icon="ASSET_MANAGER")


class ABU_OT_batch_export(Operator, BatchFolderOperator):
    "Export Assets To External File(s)"
    bl_idname = "abu.batch_export"
    bl_label = "Export Assets"

    operator_settings: PointerProperty(type=OperatorProperties)
    logic_class = BatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True, enforce_filebrowser=True)
    
    def execute(self, context):
        self.populate_asset_and_asset_names()
        if len(self.asset_names) > 0:
            self.execute_in_new_blender_instance()
        else:
            Logger.display("No asset to export")
        return {"FINISHED"}
    
    def execute_in_new_blender_instance(self):
        caller = CommandBuilder(Path(os.path.realpath(__file__)))
        for name in self.asset_names:
            caller.add_arg_value("asset_names", name)
        for _type in self.asset_types:
            caller.add_arg_value("asset_types", _type)
        caller.add_arg_value("source_file", bpy.data.filepath)
        caller.add_arg_value("filepath", self.filepath)
        caller.add_arg_value("folder", str(get_folder_from_path(self.filepath)))
        caller.add_arg_value("remove_backup", self.library_settings.remove_backup)
        caller.add_arg_value("overwrite", self.operator_settings.overwrite)
        caller.add_arg_value("individual_files", self.operator_settings.individual_files)
        caller.call()
    
    def populate_asset_and_asset_names(self):
        assets = self.asset_filter_settings.get_objects_that_satisfy_filters()
        self.asset_names = [a.name for a in assets]
        self.asset_types = [get_blend_library_name(a) for a in assets]

