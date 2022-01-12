from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, PointerProperty
from bpy.types import Operator

from asset_browser_utilities.prop.filter.settings import AssetFilterSettings
from asset_browser_utilities.prop.path import LibraryExportSettings
from asset_browser_utilities.core.preferences.helper import write_to_cache, get_from_cache
from asset_browser_utilities.helper.path import (
    get_blend_files,
    save_if_possible_and_necessary,
)

from .prop import OperatorProperties
from .logic import OperatorLogicMark, OperatorLogicUnmark


class BatchMarkOrUnmarkOperator:
    filter_glob: StringProperty(
        default="",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    operator_settings: PointerProperty(type=OperatorProperties)
    library_export_settings: PointerProperty(type=LibraryExportSettings)
    asset_filter_settings: PointerProperty(type=AssetFilterSettings)

    def _invoke(self, context):
        if self.library_export_settings.this_file_only:
            self.asset_filter_settings.init(filter_selection=True)
            return context.window_manager.invoke_props_dialog(self)
        else:
            self.asset_filter_settings.init(filter_selection=False)
            context.window_manager.fileselect_add(self)
            return {"RUNNING_MODAL"}

    def execute(self, context):
        # We write settings to cache in addon properties because this instance's properties are lost on new file load
        write_to_cache(self.asset_filter_settings, context)
        save_if_possible_and_necessary()
        self.logic_class(
            blends=get_blend_files(self),
            operator_settings=self.operator_settings,
            filter_settings=get_from_cache(AssetFilterSettings, context),
        ).execute_next_blend()
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout

        self.library_export_settings.draw(layout)
        self.operator_settings.draw(layout)
        self.asset_filter_settings.draw(layout)


class ASSET_OT_batch_mark(Operator, ImportHelper, BatchMarkOrUnmarkOperator):
    bl_idname = "asset.batch_mark"
    bl_label = "Batch Mark Assets"
    
    logic_class = OperatorLogicMark

    def invoke(self, context, event):
        return self._invoke(context)

class ASSET_OT_batch_unmark(Operator, ImportHelper, BatchMarkOrUnmarkOperator):
    bl_idname = "asset.batch_unmark"
    bl_label = "Batch Unmark Assets"
    
    logic_class = OperatorLogicUnmark

    def invoke(self, context, event):
        return self._invoke(context)
