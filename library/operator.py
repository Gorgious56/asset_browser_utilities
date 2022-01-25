from asset_browser_utilities.core.operator.helper import FilterLibraryOperator
from bpy.props import StringProperty, PointerProperty

from asset_browser_utilities.core.preferences.helper import write_to_cache, get_from_cache
from asset_browser_utilities.file.save import save_if_possible_and_necessary

from asset_browser_utilities.filter.main import AssetFilterSettings
from asset_browser_utilities.library.prop import LibraryExportSettings, LibraryType


class BatchOperator:
    filter_glob: StringProperty(
        default="",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    asset_filter_settings: PointerProperty(type=AssetFilterSettings)
    library_settings: PointerProperty(type=LibraryExportSettings)

    def _invoke(self, context, remove_backup=True, filter_assets=False):
        if self.library_settings.library_type == LibraryType.FileExternal.value:
            self.filter_glob = "*.blend"
        self.library_settings.init(remove_backup=remove_backup)
        if self.library_settings.library_type in (LibraryType.FileExternal.value, LibraryType.FolderExternal.value):
            self.asset_filter_settings.init(filter_selection=False, filter_assets=filter_assets)
            context.window_manager.fileselect_add(self)
            return {"RUNNING_MODAL"}
        else:
            self.asset_filter_settings.init(filter_selection=True, filter_assets=filter_assets)
            return context.window_manager.invoke_props_dialog(self)

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
        if self.operator_settings and hasattr(self.operator_settings, "draw"):
            self.operator_settings.draw(layout)
        self.asset_filter_settings.draw(layout)


class BatchFileOperator(FilterLibraryOperator, BatchOperator):
    filter_glob: StringProperty(
        default="*.blend",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )


class BatchFolderOperator(BatchOperator):
    pass
