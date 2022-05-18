from pathlib import Path

from asset_browser_utilities.core.operator.operation import OperationSettings
from asset_browser_utilities.core.preferences.tool import get_preferences

import bpy.app.timers
from bpy.types import OperatorFileListElement
from bpy.props import PointerProperty, StringProperty, PointerProperty, CollectionProperty, EnumProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper

from asset_browser_utilities.core.helper import copy_simple_property_group
from asset_browser_utilities.core.cache.tool import get_presets, write_to_cache, get_from_cache
from asset_browser_utilities.core.ui.message import message_box
from asset_browser_utilities.file.path import open_file_if_different_from_current
from asset_browser_utilities.file.save import save_if_possible_and_necessary, save_file_as
from asset_browser_utilities.filter.main import AssetFilterSettings
from asset_browser_utilities.library.prop import LibraryExportSettings, LibraryType
from asset_browser_utilities.preview.tool import can_preview_be_generated, is_preview_generated


class BatchExecute:
    INTERVAL = 0.2
    last_check = 10e100

    def __init__(self, operator, context):
        operator_settings = getattr(operator, "operator_settings", None)
        if operator_settings is not None:
            copy_simple_property_group(operator_settings, self)

        self.remove_backup = operator.library_settings.remove_backup
        self.filter_settings = get_from_cache(operator.asset_filter_settings.__class__)
        self.operation_settings = OperationSettings.get_from_cache()

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
        if LibraryExportSettings.get_from_cache().source == LibraryType.FileCurrent.value:
            self.assets = self.filter_settings.get_objects_that_satisfy_filters()
            self.operation_settings.execute(self.assets)

            self.execute_one_file_and_the_next_when_finished()
        else:
            if hasattr(context, "temp_override"):
                window = context.window_manager.windows[0]
                with context.temp_override(window=window):
                    self.assets = self.filter_settings.get_objects_that_satisfy_filters()
                    self.operation_settings.execute(self.assets)

                    self.execute_one_file_and_the_next_when_finished()
            else:  # For Blender < 3.2
                self.assets = self.filter_settings.get_objects_that_satisfy_filters()
                self.operation_settings.execute(self.assets)

                # Give slight delay otherwise stack overflow
                bpy.app.timers.register(self.execute_one_file_and_the_next_when_finished, first_interval=self.INTERVAL)

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

    def execute_one_file_and_the_next_when_finished(self):
        if self.assets:
            for asset in self.assets:
                self.do_on_asset(asset)
            self.save_file()
        self.execute_next_blend()

    def do_on_asset(self, asset):
        pass


def update_asset_filter_allow(self, context):
    filter_selection = not self.library_settings.source in (
        LibraryType.FolderExternal.value,
        LibraryType.FileExternal.value,
    )
    filter_selection_asset_browser = self.bl_idname not in ("ABU_OT_previews_extract",)
    self.asset_filter_settings.init(
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
        if hasattr(setting, "copy"):  # Assume it's a "complicated" property group if copy is implemented
            setting.copy(default_setting)
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
    operation_settings: PointerProperty(type=OperationSettings)
    asset_filter_settings: PointerProperty(type=AssetFilterSettings)
    library_settings: PointerProperty(type=LibraryExportSettings)
    # https://docs.blender.org/api/current/bpy.types.OperatorFileListElement.html
    files: CollectionProperty(
        type=OperatorFileListElement,
        options={"HIDDEN", "SKIP_SAVE"},
    )

    def _invoke(self, context, remove_backup=True, filter_assets=False, enforce_filebrowser=False):
        self.filter_assets = filter_assets
        update_preset(self, context)
        self.library_settings.init(remove_backup=remove_backup)
        self.operation_settings.init()
        LibraryExportSettings.get_from_cache().source = self.library_settings.source
        if self.library_settings.source in (LibraryType.FolderExternal.value, LibraryType.FileExternal.value):
            self.filter_glob = "*.blend" if self.library_settings.source == LibraryType.FileExternal.value else ""
            context.window_manager.fileselect_add(self)
            return {"RUNNING_MODAL"}
        else:
            if enforce_filebrowser:
                context.window_manager.fileselect_add(self)
                return {"RUNNING_MODAL"}
            else:
                return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        # We write settings to cache in addon properties because this instance's properties are lost on new file load
        write_to_cache(self.asset_filter_settings)
        OperationSettings.get_from_cache().copy_from(self.operation_settings)
        save_if_possible_and_necessary()
        logic = self.logic_class(self, context)
        logic.execute_next_blend()
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "preset")

        self.library_settings.draw(layout, context)
        if hasattr(self, "operator_settings") and self.operator_settings and hasattr(self.operator_settings, "draw"):
            self.operator_settings.draw(layout)
        self.asset_filter_settings.draw(layout, context)
        self.operation_settings.draw(layout, context)
