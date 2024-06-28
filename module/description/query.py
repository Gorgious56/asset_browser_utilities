from pathlib import Path
import re

import bpy

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps


class DescriptionQueryFromFileOperatorProperties(bpy.types.PropertyGroup, BaseOperatorProps):
    file_name: bpy.props.StringProperty(name="File Name", default="license.txt")  # type:ignore
    detect_author: bpy.props.BoolProperty(name="Auto-detect Author")  # type:ignore
    detect_license: bpy.props.BoolProperty(name="Auto-detect License")  # type:ignore
    detect_author_regex_query: bpy.props.StringProperty(name="Regex", default="author:(.*)")  # type:ignore
    detect_license_regex_query: bpy.props.StringProperty(name="Regex", default="license type:(.*)")  # type:ignore

    def draw(self, layout, context=None):
        layout.prop(self, "file_name", icon="FILE_TEXT")
        layout.prop(self, "detect_author", icon="USER")
        if self.detect_author:
            layout.prop(self, "detect_author_regex_query", icon="USER")
        layout.prop(self, "detect_license", icon="USER")
        if self.detect_license:
            layout.prop(self, "detect_license_regex_query", icon="USER")

    def run_on_asset(self, asset):
        folder = Path(bpy.data.filepath).parent
        file = folder / self.file_name
        if file.exists():
            with open(file, "r") as f:
                lines = f.read()
                asset.asset_data.description = lines
                Logger.display(f"Set {asset.name}'s description to '{lines}'")

                for detect, pattern in zip(
                    ("author", "license"),
                    (
                        self.detect_author_regex_query or r"\* author:\s*(.*?)\s*\(",
                        self.detect_license_regex_query or r"\* license type:\s*([^(\n]+)",
                    ),
                ):
                    if getattr(self, f"detect_{detect}"):
                        match = re.search(pattern, lines)
                        if match:
                            setattr(asset.asset_data, detect, match.group(1).strip())
                            Logger.display(
                                f"Automatically Set {asset.name}'s {detect} to '{getattr(asset.asset_data, detect)}'"
                            )
        else:
            return False


class ABU_OT_description_query_from_file(bpy.types.Operator, BatchFolderOperator):
    bl_idname = "abu.description_query_from_file"
    bl_label = "Batch Query Description From File"
    bl_description = "Batch Set Description. The contents of the specified file name are written as the description. The file must be in the same directory as the asset"

    operator_settings: bpy.props.PointerProperty(type=DescriptionQueryFromFileOperatorProperties)  # type:ignore

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
