from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator


class CopyrightSetBatchExecute(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        copyright = get_current_operator_properties().copyright
        for asset in self.assets:
            asset.asset_data.copyright = copyright
            Logger.display(f"Set {repr(asset)}'s copyright to '{copyright}'")
        self.save_file()
        self.execute_next_file()


class CopyrightSetOperatorProperties(PropertyGroup):
    copyright: StringProperty(name="Copyright")

    def draw(self, layout, context=None):
        layout.prop(self, "copyright", icon="USER")


class ABU_OT_copyright_set(Operator, BatchFolderOperator):
    bl_idname = "abu.copyright_set"
    bl_label = "Batch Set Copyright"
    bl_description = "Batch Set Copyright. Leave Field Empty to remove copyright"

    operator_settings: PointerProperty(type=CopyrightSetOperatorProperties)
    logic_class = CopyrightSetBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
