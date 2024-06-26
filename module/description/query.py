from pathlib import Path

import bpy

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps


class DescriptionQueryFromFileOperatorProperties(bpy.types.PropertyGroup, BaseOperatorProps):
    file_name: bpy.props.StringProperty(name="File Name")  # type:ignore

    def draw(self, layout, context=None):
        layout.prop(self, "file_name", icon="FILE_TEXT")

    def run_on_asset(self, asset):
        folder = Path(bpy.data.filepath).parent
        file = folder / self.file_name
        if file.exists():
            with open(file, "r") as f:
                lines = f.read()
                asset.asset_data.description = lines
                Logger.display(f"Set {asset.name}'s description to '{lines}'")
        else:
            return False


class ABU_OT_description_query_from_file(bpy.types.Operator, BatchFolderOperator):
    bl_idname = "abu.description_query_from_file"
    bl_label = "Batch Query Description From File"
    bl_description = "Batch Set Description. The contents of the specified file name are written as the description. The file must be in the same directory as the asset"

    operator_settings: bpy.props.PointerProperty(type=DescriptionQueryFromFileOperatorProperties)  # type:ignore

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
