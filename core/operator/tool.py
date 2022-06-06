from asset_browser_utilities.asset.prop import SelectedAssetFiles
from asset_browser_utilities.core.operator.prop import CurrentOperatorProperty
from asset_browser_utilities.core.log.logger import Logger

from asset_browser_utilities.core.operator.operation import OperationSettings
from asset_browser_utilities.core.preferences.tool import get_preferences

import bpy.app.timers
from bpy.types import OperatorFileListElement
from bpy.props import StringProperty, CollectionProperty, EnumProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper

from asset_browser_utilities.core.tool import copy_simple_property_group
from asset_browser_utilities.core.cache.tool import get_presets, get_from_cache
from asset_browser_utilities.core.ui.message import message_box
from asset_browser_utilities.file.path import open_file_if_different_from_current
from asset_browser_utilities.file.save import save_if_possible_and_necessary, save_file_as
from asset_browser_utilities.filter.main import AssetFilterSettings
from asset_browser_utilities.library.prop import LibraryExportSettings, LibraryType
from asset_browser_utilities.preview.tool import can_preview_be_generated, is_preview_generated


class BatchExecute:
    INTERVAL = 0.2
    last_check = 10e100

    def __init__(self):
        self.blends = get_from_cache(LibraryExportSettings).get_blend_files()
        self.blend = None
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
        Logger.display(f"{len(self.blends)} file{'s' if len(self.blends) > 1 else ''} left")

        self.open_next_blend()
        if get_from_cache(LibraryExportSettings).source == LibraryType.FileCurrent.value:
            self.assets = get_from_cache(AssetFilterSettings).get_objects_that_satisfy_filters()
            get_from_cache(OperationSettings).execute(self.assets)

            self.execute_one_file_and_the_next_when_finished()
        else:
            if hasattr(context, "temp_override"):
                window = context.window_manager.windows[0]
                with context.temp_override(window=window):
                    self.assets = get_from_cache(AssetFilterSettings).get_objects_that_satisfy_filters()
                    get_from_cache(OperationSettings).execute(self.assets)

                    self.execute_one_file_and_the_next_when_finished()
            else:  # For Blender < 3.2
                self.assets = get_from_cache(AssetFilterSettings).get_objects_that_satisfy_filters()
                get_from_cache(OperationSettings).execute(self.assets)

                # Give slight delay otherwise stack overflow
                bpy.app.timers.register(self.execute_one_file_and_the_next_when_finished, first_interval=self.INTERVAL)

    def save_file(self):
        save_file_as(str(self.blend), remove_backup=get_from_cache(LibraryExportSettings).remove_backup)

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

    def execute_one_file_and_the_next_when_finished(self):
        if self.assets:
            for asset in self.assets:
                self.do_on_asset(asset)
            self.save_file()
        self.execute_next_blend()

    def do_on_asset(self, asset):
        pass


def update_asset_filter_allow(self, context):
    filter_selection = not get_from_cache(LibraryExportSettings).source in (
        LibraryType.FolderExternal.value,
        LibraryType.FileExternal.value,
    )
    filter_selection_asset_browser = self.bl_idname not in ("ABU_OT_previews_extract",)
    get_from_cache(AssetFilterSettings).init(
        context,
        filter_selection=filter_selection,
        filter_assets=self.filter_assets,
        filter_selection_allow_asset_browser=filter_selection_asset_browser,
    )


def update_preset(self, context):
    preset_name = self.preset
    if preset_name == "ABU_DEFAULT":
        preset = get_preferences().defaults
    else:
        preset = next(p for p in get_preferences().presets if p.name == preset_name)
    for attr in preset.__annotations__:
        if attr == "library_settings":
            continue
        if not hasattr(self, attr):
            continue
        default_setting = getattr(preset, attr)
        setting = getattr(self, attr)
        if hasattr(setting, "copy_from"):  # Assume it's a "complicated" property group if copy_from is implemented
            setting.copy_from(default_setting)
        else:
            copy_simple_property_group(default_setting, setting)
    update_asset_filter_allow(self, context)


class BatchFolderOperator(ImportHelper):
    filter_glob: StringProperty(
        default="",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    filter_assets: BoolProperty()
    preset: EnumProperty(name="Preset", items=get_presets, update=update_preset)
    source: StringProperty()
    # https://docs.blender.org/api/current/bpy.types.OperatorFileListElement.html
    files: CollectionProperty(type=OperatorFileListElement, options={"HIDDEN", "SKIP_SAVE"})

    def _invoke(self, context, remove_backup=True, filter_assets=False, enforce_filebrowser=False):
        self.filter_assets = filter_assets

        update_preset(self, context)

        get_from_cache(OperationSettings).init()

        if hasattr(self, "operator_settings"):
            get_from_cache(CurrentOperatorProperty).class_name = str(self.operator_settings.__class__)

        library_settings = get_from_cache(LibraryExportSettings)
        library_settings.init(remove_backup=remove_backup)
        if self.source != "":
            library_settings.source = self.source

        selected_asset_files_prop = get_from_cache(SelectedAssetFiles)
        selected_asset_files_prop.init()
        for selected_asset_file in bpy.context.selected_asset_files:
            selected_asset_files_prop.add(selected_asset_file.id_type, selected_asset_file.local_id)

        if library_settings.source in (LibraryType.FolderExternal.value, LibraryType.FileExternal.value):
            self.filter_glob = "*.blend" if library_settings.source == LibraryType.FileExternal.value else ""
            context.window_manager.fileselect_add(self)
            return {"RUNNING_MODAL"}
        else:
            if enforce_filebrowser:
                context.window_manager.fileselect_add(self)
                return {"RUNNING_MODAL"}
            else:
                return context.window_manager.invoke_props_dialog(self)

    def write_filepath_to_cache(self):
        library_settings = get_from_cache(LibraryExportSettings)
        library_settings.files = self.files
        library_settings.filepath = self.filepath

    def execute(self, context):
        self.write_filepath_to_cache()
        save_if_possible_and_necessary()
        logic = self.logic_class()
        logic.execute_next_blend()
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "preset")

        get_from_cache(LibraryExportSettings).draw(layout, context)
        if hasattr(self, "operator_settings") and self.operator_settings and hasattr(self.operator_settings, "draw"):
            get_from_cache(self.operator_settings.__class__).draw(layout)
        get_from_cache(AssetFilterSettings).draw(layout, context)
        get_from_cache(OperationSettings).draw(layout, context)
