from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, PointerProperty
from bpy.types import Operator

from asset_browser_utilities.filter.main import AssetFilterSettings
from asset_browser_utilities.core.preferences.helper import write_to_cache, get_from_cache
from asset_browser_utilities.file.path import (
    get_blend_files,
    save_if_possible_and_necessary,
)
from asset_browser_utilities.core.operator.helper import FilterLibraryOperator
from .prop import OperatorProperties
from .helper import OperatorLogicMark, OperatorLogicUnmark


class BatchMarkOrUnmarkOperator(FilterLibraryOperator):
    filter_glob: StringProperty(
        default="",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    operator_settings: PointerProperty(type=OperatorProperties)

    def execute(self, context):
        # We write settings to cache in addon properties because this instance's properties are lost on new file load
        write_to_cache(self.asset_filter_settings, context)
        save_if_possible_and_necessary()
        self.logic_class(
            blends=get_blend_files(self),
            operator_settings=self.operator_settings,
            filter_settings=get_from_cache(AssetFilterSettings, context),
            library_settings=self.library_settings,
        ).execute_next_blend()
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout

        self.library_settings.draw(layout)
        self.operator_settings.draw(layout)
        self.asset_filter_settings.draw(layout)


class ASSET_OT_batch_mark(Operator, ImportHelper, BatchMarkOrUnmarkOperator):
    bl_idname = "asset.batch_mark"
    bl_label = "Batch Mark Assets"

    logic_class = OperatorLogicMark

    def invoke(self, context, event):
        self.operator_settings.mark = True
        return self._invoke(context)


class ASSET_OT_batch_unmark(Operator, ImportHelper, BatchMarkOrUnmarkOperator):
    bl_idname = "asset.batch_unmark"
    bl_label = "Batch Unmark Assets"

    logic_class = OperatorLogicUnmark

    def invoke(self, context, event):
        return self._invoke(context)
