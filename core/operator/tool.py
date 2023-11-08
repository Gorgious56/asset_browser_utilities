from asset_browser_utilities.module.asset.prop import SelectedAssetFiles
from asset_browser_utilities.core.operator.prop import CurrentOperatorProperty
from asset_browser_utilities.core.log.logger import Logger

from asset_browser_utilities.core.preferences.tool import get_preferences

import bpy.app.timers
from bpy.types import OperatorFileListElement
from bpy.props import StringProperty, CollectionProperty, EnumProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper

from asset_browser_utilities.core.tool import copy_simple_property_group
from asset_browser_utilities.core.cache.tool import get_current_operator_properties, get_presets, get_from_cache
from asset_browser_utilities.core.ui.message import message_box
from asset_browser_utilities.core.file.path import open_file_if_different_from_current
from asset_browser_utilities.core.file.save import save_if_possible_and_necessary, save_file_as
from asset_browser_utilities.core.filter.main import AssetFilterSettings
from asset_browser_utilities.core.library.prop import LibraryExportSettings, LibraryType
from asset_browser_utilities.module.preview.tool import can_preview_be_generated, is_preview_generated


class BatchExecute:
    INTERVAL = 0.01
    INTERVAL_PREVIEW = 0.05

    def __init__(self, file_extension="blend"):
        self.files = get_from_cache(LibraryExportSettings).get_files(file_extension)
        self.file = None
        self.assets = []

    def callback(self):
        [a.tag_redraw() for a in bpy.context.screen.areas if a.ui_type == "ASSETS" and hasattr(bpy.context, "screen")]

    def execute_next_file(self):
        library_export_settings = get_from_cache(LibraryExportSettings)
        if not self.files:
            if not bpy.app.background:
                if library_export_settings.filepath_start != "":
                    open_file_if_different_from_current(str(library_export_settings.filepath_start))
                # Wait a little bit for context to initialize
                bpy.app.timers.register(lambda: message_box(message="Work completed !"), first_interval=self.INTERVAL)
            bpy.app.timers.register(self.callback, first_interval=self.INTERVAL)
            return
        Logger.display(f"{len(self.files)} file{'s' if len(self.files) > 1 else ''} left")
        if self.open_next_file():
            if library_export_settings.source == LibraryType.FileCurrent.value:
                self.assets = get_from_cache(AssetFilterSettings).get_objects_that_satisfy_filters()

                self.execute_one_file_and_the_next_when_finished()
            else:
                self.assets = get_from_cache(AssetFilterSettings).get_objects_that_satisfy_filters()
                # Wait a little bit for context to initialize
                bpy.app.timers.register(self.execute_one_file_and_the_next_when_finished, first_interval=self.INTERVAL)
        else:
            self.execute_next_file()

    def save_file(self, filepath=None):
        if filepath is None:
            filepath = str(self.file)
        save_file_as(filepath, remove_backup=get_from_cache(LibraryExportSettings).remove_backup)

    def open_next_file(self):
        self.file = self.files.pop(0)
        open_file_if_different_from_current(str(self.file))
        return True

    def sleep_until_previews_are_done_and_execute_next_file(self):
        while self.assets:
            if hasattr(bpy.app, "is_job_running"):  # Blender 3.3+
                if bpy.app.is_job_running("RENDER_PREVIEW"):
                    return self.INTERVAL_PREVIEW
                break
            else:  # Blender <= 3.2
                if not can_preview_be_generated(self.assets[0]) or is_preview_generated(self.assets[0]):
                    self.assets.pop(0)
                else:
                    return self.INTERVAL_PREVIEW
        self.save_file()
        self.execute_next_file()
        return None

    def execute_one_file_and_the_next_when_finished(self):
        if self.assets:
            for asset in self.assets:
                self.do_on_asset(asset)
            self.save_file()
        self.execute_next_file()

    def do_on_asset(self, asset):
        pass


def update_preset(self, context):
    preset_name = self.preset
    if preset_name == "ABU_DEFAULT":
        preset = get_preferences().defaults
    else:
        preset = next(p for p in get_preferences().presets if p.name == preset_name)
    current_op_properties = get_current_operator_properties()
    for attr in preset.__annotations__:
        if attr == "library_settings":
            continue
        default_properties = getattr(preset, attr)
        if attr.startswith("op_") and not type(default_properties) == type(current_op_properties):
            continue
        setting = get_from_cache(type(default_properties))
        if hasattr(setting, "copy_from"):  # Assume it's a "complicated" property group if copy_from is implemented
            setting.copy_from(default_properties)
        else:
            copy_simple_property_group(default_properties, setting)


class BatchFolderOperator(ImportHelper):
    bl_options: set[str] = {"UNDO"}
    ui_library = LibraryType.All
    file_extension = "blend"
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
    directory: StringProperty()
    logic_class = BatchExecute

    def _invoke(
        self,
        context,
        remove_backup=True,
        filter_assets=False,
        filter_type=True,
        filter_selection=True,
        filter_name=True,
        enforce_filebrowser=False,
        init_operator_settings_arguments: dict = None,
    ):
        self.filter_assets = filter_assets
        self.filter_types = filter_type
        self.filter_selection = filter_selection
        self.filter_name = filter_name

        update_preset(self, context)
        self.update_asset_filter_allow()
        self.init_operator_settings(init_operator_settings_arguments)
        self.init_selected_asset_files(context)
        library_settings = self.init_library_settings(remove_backup)

        if library_settings.source in (LibraryType.FolderExternal.value, LibraryType.FileExternal.value):
            self.filter_glob = (
                ("*." + self.file_extension) if library_settings.source == LibraryType.FileExternal.value else ""
            )
            context.window_manager.fileselect_add(self)
            return {"RUNNING_MODAL"}
        else:
            if enforce_filebrowser:
                context.window_manager.fileselect_add(self)
                return {"RUNNING_MODAL"}
            else:
                return context.window_manager.invoke_props_dialog(self)

    def init_operator_settings(self, init_args):
        if hasattr(self, "operator_settings"):
            get_from_cache(CurrentOperatorProperty).class_name = str(self.operator_settings.__class__)
        current_operator_settings = get_current_operator_properties()
        if hasattr(current_operator_settings, "init"):
            if init_args is not None:
                current_operator_settings.init(**init_args)
            else:
                current_operator_settings.init()

    def init_library_settings(self, remove_backup):
        library_settings = get_from_cache(LibraryExportSettings)
        library_settings.init(remove_backup=remove_backup)
        if self.source != "":
            library_settings.source = self.source
        library_settings.filepath_start = bpy.data.filepath
        return library_settings

    def init_selected_asset_files(self, context):
        selected_asset_files_prop = get_from_cache(SelectedAssetFiles)
        selected_asset_files_prop.init()
        if context.active_file is not None:
            selected_asset_files_prop.set_active(context.active_file.id_type, context.active_file.local_id)
        for selected_asset_file in bpy.context.selected_asset_files:
            selected_asset_files_prop.add(selected_asset_file.id_type, selected_asset_file.local_id)

    def execute(self, context):
        self.write_filepath_to_cache()
        save_if_possible_and_necessary()
        logic = self.logic_class(self.file_extension)
        logic.execute_next_file()
        return {"FINISHED"}

    def write_filepath_to_cache(self):
        library_settings = get_from_cache(LibraryExportSettings)
        library_settings.folder = self.directory
        library_settings.files = [self.directory + f.name for f in self.files]

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "preset")

        get_from_cache(LibraryExportSettings).draw(layout, context)
        if hasattr(self, "operator_settings") and self.operator_settings and hasattr(self.operator_settings, "draw"):
            get_from_cache(self.operator_settings.__class__).draw(layout)
        get_from_cache(AssetFilterSettings).draw(layout, context)

    def update_asset_filter_allow(self):
        filter_selection = (
            not get_from_cache(LibraryExportSettings).source
            in (
                LibraryType.FolderExternal.value,
                LibraryType.FileExternal.value,
            )
            and self.filter_selection
        )
        get_from_cache(AssetFilterSettings).init_asset_filter_settings(
            filter_selection=filter_selection,
            filter_assets=self.filter_assets,
            filter_types=self.filter_types,
            filter_name=self.filter_name,
        )
