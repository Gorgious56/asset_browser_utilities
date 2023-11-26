import queue

import bpy.app.timers
from bpy.types import OperatorFileListElement
from bpy.props import StringProperty, CollectionProperty, EnumProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper

from asset_browser_utilities.core.preferences.tool import get_preferences
from asset_browser_utilities.core.tool import copy_simple_property_group
from asset_browser_utilities.core.cache.tool import get_current_operator_properties, get_presets, get_from_cache
from asset_browser_utilities.core.filter.main import AssetFilterSettings
from asset_browser_utilities.core.library.prop import LibraryExportSettings, LibraryType
from asset_browser_utilities.core.operator.prop import CurrentOperatorProperty
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.console.builder import CommandBuilder
from asset_browser_utilities.core.console import command_execute_on_blend_file
from asset_browser_utilities.core.threading.tool import ThreadManager

from asset_browser_utilities.module.asset.prop import SelectedAssetFiles


class BaseOperatorProps:
    def get_assets(self):
        return get_from_cache(AssetFilterSettings).get_objects_that_satisfy_filters()

    def run_in_file(self, attributes=None):
        assets = self.get_assets()
        if not assets:
            return
        for asset in assets:
            self.run_on_asset(asset)


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
    file_for_command = __file__

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
        if context.asset:
            selected_asset_files_prop.set_active(context.asset.local_id)
        for selected_asset in context.selected_assets:
            selected_asset_files_prop.add(selected_asset.local_id)
            
    def on_finish(self):
        return

    def modal(self, context, event):
        [a.tag_redraw() for a in context.screen.areas]
        if context.window_manager.abu_progress.factor >= 1:
            self.on_finish()
            return {"FINISHED"}
        return {"PASS_THROUGH"}

    def execute(self, context):
        bpy.ops.wm.save_userpref()
        if get_from_cache(LibraryExportSettings).source == LibraryType.FileCurrent.value:
            get_current_operator_properties().run_in_file()
        else:
            self.run_in_threads(context)
        context.window_manager.event_timer_add(time_step=0.1, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

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

    def filter_files(self, files):
        return files

    def thread_manager_callback(self, context):
        context.window_manager.abu_progress.update_for_task_finished()

    def run_in_threads(self, context):
        files = get_from_cache(LibraryExportSettings).get_files("blend")
        files = self.filter_files(files)
        file_queue = queue.Queue(maxsize=len(files))
        for file in files:
            file_queue.put(file)

        def run(index=-1):
            caller = CommandBuilder(
                script_filepath=command_execute_on_blend_file.__file__,
                blend_filepath=file_queue.get(),
            )
            caller.add_arg_value("thread_index", index)
            caller.call()

        ThreadManager.init(
            run,
            file_queue.qsize(),
            callback=lambda context=context: self.thread_manager_callback(context),
        )
        ThreadManager.run(wait_for_execution=False)
        context.window_manager.abu_progress.init(tasks_total=len(files))
