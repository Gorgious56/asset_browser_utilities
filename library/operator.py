from asset_browser_utilities.core.operator.helper import FilterLibraryOperator
from bpy.props import StringProperty

from asset_browser_utilities.core.preferences.helper import write_to_cache, get_from_cache
from asset_browser_utilities.file.save import save_if_possible_and_necessary


class BatchOperator(FilterLibraryOperator):
    filter_glob: StringProperty(
        default="",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        # We write settings to cache in addon properties because this instance's properties are lost on new file load
        write_to_cache(self.asset_filter_settings, context)
        save_if_possible_and_necessary()
        self.logic_class(
            blends=self.library_settings.get_blend_files(self.filepath),
            operator_settings=getattr(self, "operator_settings", None),
            filter_settings=get_from_cache(self.asset_filter_settings.__class__, context),
            library_settings=self.library_settings,
            callback=lambda c: [
                a.tag_redraw() for a in c.screen.areas if a.ui_type == "ASSETS" and hasattr(c, "screen")
            ],
        ).execute_next_blend()
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout

        self.library_settings.draw(layout)
        if self.operator_settings:
            self.operator_settings.draw(layout)
        self.asset_filter_settings.draw(layout)
