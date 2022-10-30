from asset_browser_utilities.core.cache.tool import get_current_operator_properties, get_from_cache
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.module.operation.prop import OperationSettings
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator


class OperationExecute(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        if not self.assets:
            self.execute_next_blend()
            return
        operator_properties = get_current_operator_properties()
        operator_properties.settings.execute(self.assets)

        self.save_file()
        self.execute_next_blend()


class OperationCustomOperatorProperties(PropertyGroup):
    MAX_OPS = 15

    settings: PointerProperty(type=OperationSettings)

    def draw(self, layout, context=None):
        self.settings.draw(layout, context)

    def init(self):
        for _ in range(self.MAX_OPS):
            self.settings.operations.add()


class ABU_OT_operation_custom(Operator, BatchFolderOperator):
    bl_idname = "abu.operation_custom"
    bl_label = "Execute Custom Operations"
    bl_options = {"REGISTER", "UNDO"}

    operator_settings: PointerProperty(type=OperationCustomOperatorProperties)
    logic_class = OperationExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
