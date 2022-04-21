from pathlib import Path

import bpy.app.timers
from bpy.types import OperatorFileListElement
from bpy.props import PointerProperty, StringProperty, PointerProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper

from asset_browser_utilities.core.helper import copy_simple_property_group
from asset_browser_utilities.core.preferences.helper import write_to_cache, get_from_cache
from asset_browser_utilities.core.ui.message import message_box
from asset_browser_utilities.file.path import open_file_if_different_from_current
from asset_browser_utilities.file.save import save_if_possible_and_necessary, save_file_as
from asset_browser_utilities.filter.main import AssetFilterSettings
from asset_browser_utilities.library.prop import LibraryExportSettings, LibraryType, LibraryPG
from asset_browser_utilities.preview.helper import can_preview_be_generated, is_preview_generated

## Where is this used ?
class FilterLibraryOperator:
    asset_filter_settings: PointerProperty(type=AssetFilterSettings)
    library_settings: PointerProperty(type=LibraryExportSettings)

    def _invoke(self, context, remove_backup=True, filter_assets=False):
        self.library_settings.init(remove_backup=remove_backup)
        LibraryPG.set_library_type(context, self.library_settings.library_type)
        if self.library_settings.library_type in (LibraryType.FileExternal.value, LibraryType.FolderExternal.value):
            self.asset_filter_settings.init(context, filter_selection=False, filter_assets=filter_assets)
            context.window_manager.fileselect_add(self)
            return {"RUNNING_MODAL"}
        else:
            self.asset_filter_settings.init(context, filter_selection=True, filter_assets=filter_assets)
            return context.window_manager.invoke_props_dialog(self)


class BatchExecute:
    INTERVAL = 0.2
    last_check = 10e100

    def __init__(self, operator, context):
        operator_settings = getattr(operator, "operator_settings", None)
        if operator_settings is not None:
            copy_simple_property_group(operator_settings, self)

        self.remove_backup = operator.library_settings.remove_backup
        self.filter_settings = get_from_cache(operator.asset_filter_settings.__class__, context)

        filepath = Path(operator.filepath)
        if filepath.is_file():
            filepath = filepath.parent

        self.blends = operator.library_settings.get_blend_files(
            folder=filepath,
            filepaths=[f.name for f in operator.files],
        )
        self.blend = None

        # This is called when everything is finished.
        self.assets = []

    def callback(self, context):
        [a.tag_redraw() for a in context.screen.areas if a.ui_type == "ASSETS" and hasattr(context, "screen")]

    def execute_next_blend(self):
        context = bpy.context
        if not self.blends:
            print("Work completed")
            message_box(message="Work completed !")
            self.callback(context)
            return
        print(f"{len(self.blends)} file{'s' if len(self.blends) > 1 else ''} left")

        self.open_next_blend()
        self.assets = self.filter_settings.get_objects_that_satisfy_filters()

        # Give slight delay otherwise stack overflow
        bpy.app.timers.register(lambda: self.execute_one_file_and_the_next_when_finished(context), first_interval=self.INTERVAL)

    def save_file(self):
        save_file_as(str(self.blend), remove_backup=self.remove_backup)

    def open_next_blend(self):
        self.blend = self.blends.pop(0)
        open_file_if_different_from_current(str(self.blend))

    def sleep_until_previews_are_done_and_execute_next_file(self):
        while self.assets:
            if not can_preview_be_generated(self.assets[0]) or is_preview_generated(self.assets[0]):
                self.assets.pop(0)
            else:
                return self.INTERVAL
        self.save_file()
        self.execute_next_blend()
        return None

    def execute_one_file_and_the_next_when_finished(self, context):
        if self.assets:
            for asset in self.assets:
                self.do_on_asset(asset)
            self.save_file()
        self.execute_next_blend()

    def do_on_asset(self, asset):
        pass


class BatchFolderOperator(ImportHelper):
    filter_glob: StringProperty(
        default="",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    asset_filter_settings: PointerProperty(type=AssetFilterSettings)
    library_settings: PointerProperty(type=LibraryExportSettings)
    # https://docs.blender.org/api/current/bpy.types.OperatorFileListElement.html
    files: CollectionProperty(
        type=OperatorFileListElement,
        options={"HIDDEN", "SKIP_SAVE"},
    )

    def _invoke(self, context, remove_backup=True, filter_assets=False):
        self.library_settings.init(remove_backup=remove_backup)
        LibraryPG.set_library_type(context, self.library_settings.library_type)
        print(context.window_manager)
        if self.library_settings.library_type in (LibraryType.FolderExternal.value, LibraryType.FileExternal.value):
            self.filter_glob = "*.blend" if self.library_settings.library_type == LibraryType.FileExternal.value else ""
            self.asset_filter_settings.init(context, filter_selection=False, filter_assets=filter_assets)
            context.window_manager.fileselect_add(self)
            return {"RUNNING_MODAL"}
        else:
            self.asset_filter_settings.init(context, filter_selection=True, filter_assets=filter_assets)
            return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        # We write settings to cache in addon properties because this instance's properties are lost on new file load
        write_to_cache(self.asset_filter_settings, context)
        save_if_possible_and_necessary()
        logic = self.logic_class(self, context)
        logic.execute_next_blend()
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout

        self.library_settings.draw(layout)
        if hasattr(self, "operator_settings") and self.operator_settings and hasattr(self.operator_settings, "draw"):
            self.operator_settings.draw(layout)
        self.asset_filter_settings.draw(layout, context)
