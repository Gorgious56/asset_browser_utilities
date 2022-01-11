import json
import subprocess
import os
from pathlib import Path
import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator, PropertyGroup
from bpy.props import StringProperty, BoolProperty, EnumProperty, PointerProperty

from asset_browser_utilities.prop.filter.settings import AssetFilterSettings
from asset_browser_utilities.helper.path import (
    is_this_current_file,
    save_if_possible_and_necessary,
)
from .logic import OperatorLogic


class ExportProperties(PropertyGroup):
    individual_files: BoolProperty(
        name="Place Assets in Individual Files",
        description="If this is ON, each asset will be exported to an individual file in the target directory",
    )
    prevent_backup: BoolProperty(
        name="Remove Backup",
        description="Check to automatically delete the creation of backup files when 'Save Versions' is enabled in the preferences\nThis will prevent duplicating files when they are overwritten\nWarning : Backup files ending in .blend1 will be deleted permantently",
        default=True,
    )
    overwrite: BoolProperty(
        name="Overwrite Assets",
        description="Check to overwrite objects if an object with the same name already exists in target file",
        default=True,
    )
    open_in_new_file: BoolProperty(
        default=True,
        name="Open New Blender Instance",
        description="If checked, the file where the assets will be exported will be opened in a new blender instance",
    )

    def draw(self, layout):
        layout.prop(self, "open_in_new_file", icon="WINDOW")
        layout.prop(self, "individual_files", icon="NEWFOLDER")
        layout.prop(self, "prevent_backup", icon="TRASH")
        layout.prop(self, "overwrite", icon="ASSET_MANAGER")


class ASSET_OT_export(Operator, ExportHelper):
    bl_idname = "asset.export"
    bl_label = "Export Assets"

    filter_glob: StringProperty(
        default="*.blend",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    filename_ext = ".blend"

    operator_settings: PointerProperty(type=ExportProperties)
    asset_filter_settings: PointerProperty(type=AssetFilterSettings)

    def invoke(self, context, event):
        self.asset_filter_settings.init(filter_selection=True, filter_assets=True)
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        filepath = self.filepath
        if is_this_current_file(filepath):
            return {"FINISHED"}
        source_file = bpy.data.filepath

        assets = self.asset_filter_settings.get_objects_that_satisfy_filters()
        asset_names = [a.name for a in assets]
        asset_types = [type(a).__name__ for a in assets]
        del assets  # Don't keep this in memory since it will be invalidated by loading a new file

        if self.operator_settings.open_in_new_file:
            script_file = Path(os.path.realpath(__file__))
            directory = script_file.parent
            command_path = os.path.join(directory, "command.py")

            call = "blender --python " + json.dumps(command_path) + " --"
            call += " --asset_names"
            for name in asset_names:
                call += f" {json.dumps(name)}"
            call += " --asset_types"
            for _type in asset_types:
                call += f" {json.dumps(_type)}"
            call += " --source_file " + json.dumps(source_file)
            call += " --filepath " + json.dumps(self.filepath)
            call += " --prevent_backup " + json.dumps(self.operator_settings.prevent_backup)
            call += " --overwrite " + json.dumps(self.operator_settings.overwrite)
            call += " --individual_files " + json.dumps(self.operator_settings.individual_files)
            subprocess.call(call)
        else:
            save_if_possible_and_necessary()
            operator_logic = OperatorLogic(
                asset_names,
                asset_types,
                source_file,
                filepath,
                self.operator_settings.prevent_backup,
                self.operator_settings.overwrite,
                self.operator_settings.individual_files,
            )
            operator_logic.execute()

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        self.operator_settings.draw(layout)
        self.asset_filter_settings.draw(layout)
