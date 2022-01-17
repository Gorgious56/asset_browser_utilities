from asset_browser_utilities.core.operator.helper import FilterLibraryOperator
from bpy.props import StringProperty

from asset_browser_utilities.filter.main import AssetFilterSettings
from asset_browser_utilities.core.preferences.helper import write_to_cache, get_from_cache
from asset_browser_utilities.file.path import (
    get_blend_files,
    save_if_possible_and_necessary,
)


class BatchOperator(FilterLibraryOperator):
    filter_glob: StringProperty(
        default="",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    operator_settings = None

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
        [a.tag_redraw() for a in context.screen.areas if a.ui_type == "ASSETS"]
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout

        self.library_settings.draw(layout)
        if self.operator_settings:
            self.operator_settings.draw(layout)
        self.asset_filter_settings.draw(layout)
