import functools
import numpy as np
import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, PointerProperty
from bpy.types import Operator, PropertyGroup

from asset_browser_utilities.prop.filter.settings import AssetFilterSettings
from asset_browser_utilities.prop.path import LibraryExportSettings
from asset_browser_utilities.ui.message import message_box
from asset_browser_utilities.core.preferences.helper import write_to_cache, get_from_cache
from asset_browser_utilities.helper.path import (
    get_blend_files,
    save_if_possible_and_necessary,
    save_file_as,
    open_file_if_different_from_current,
)


INTERVAL = 0.2


class BatchMarkOrUnmarkProperties(PropertyGroup):
    prevent_backup: BoolProperty(
        name="Remove Backup",
        description="Check to automatically delete the creation of backup files when 'Save Versions' is enabled in the preferences\nThis will prevent duplicating files when they are overwritten\nWarning : Backup files ending in .blend1 will be deleted permantently",
        default=True,
    )

    overwrite: BoolProperty(
        name="Overwrite assets",
        description="Check to re-mark assets and re-generate preview if the item is already an asset",
        default=False,
    )

    mark: BoolProperty(
        name="Mark",
        description="Check to Mark existing assets rather than unmarking items",
        default=False,
    )

    generate_previews: BoolProperty(
        default=True,
        name="Generate Previews",
        description="When marking assets, automatically generate a preview\nUncheck to mark assets really fast",
    )
    
    def draw(self, layout):
        layout.prop(self, "prevent_backup", icon="TRASH")
        if self.mark:
            layout.prop(self, "overwrite", icon="ASSET_MANAGER")
            layout.prop(self, "generate_previews", icon="RESTRICT_RENDER_OFF")



class ASSET_OT_batch_mark_or_unmark(Operator, ImportHelper):
    bl_idname = "asset.batch_mark_or_unmark"
    bl_label = "Batch Mark or Unmark Assets"

    filter_glob: StringProperty(
        default="",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    operator_settings: PointerProperty(type=BatchMarkOrUnmarkProperties)
    library_export_settings: PointerProperty(type=LibraryExportSettings)
    asset_filter_settings: PointerProperty(type=AssetFilterSettings)

    def invoke(self, context, event):
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
        OperatorLogic(
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


class OperatorLogic:
    def __init__(self, blends, operator_settings, filter_settings):
        self.prevent_backup = operator_settings.prevent_backup
        self.overwrite = operator_settings.overwrite
        self.mark = operator_settings.mark
        self.generate_previews = operator_settings.generate_previews

        self.filter_settings = filter_settings

        self.blends = blends
        self.blend = None
        self.assets = []

    def execute_next_blend(self):
        if not self.blends:
            print("Work completed")
            message_box(message="Work completed !")
            return
        print(f"{len(self.blends)} file{'s' if len(self.blends) > 1 else ''} left")

        self.open_next_blend()
        self.assets = self.filter_settings.get_objects_that_satisfy_filters()

        # Give slight delay otherwise stack overflow
        bpy.app.timers.register(self.mark_or_unmark, first_interval=INTERVAL)

    def mark_or_unmark(self):
        if self.mark:
            self.mark_assets()
        else:
            self.unmark_assets()
            self.execute_next_blend()

    def save_file(self):
        save_file_as(str(self.blend), remove_backup=self.prevent_backup)

    def open_next_blend(self):        
        self.blend = self.blends.pop(0)
        open_file_if_different_from_current(str(self.blend))

    def mark_assets(self):    
        self.assets = [a for a in self.assets if a.asset_data is None or self.overwrite]

        if not self.assets:  # We don't mark any asset, don't bother saving the file
            print("No asset to mark")
            self.execute_next_blend()
            return

        if self.generate_previews:
            self.mark_assets_with_previews()
        else:
            self.mark_assets_without_previews()

    def mark_assets_with_previews(self):
        for asset in self.assets:                
            asset.asset_mark()                
            asset.asset_generate_preview()
            print(f"Mark {asset.name}")
        bpy.app.timers.register(self.sleep_until_previews_are_done)
        
    def sleep_until_previews_are_done(self):
        while self.assets:  # Check if all previews have been generated
            preview = self.assets[0].preview
            if not preview:
                self.assets[0].asset_generate_preview()
            arr = np.zeros((preview.image_size[0] * preview.image_size[1]) * 4, dtype=np.float32)
            preview.image_pixels_float.foreach_get(arr)
            if np.all((arr == 0)):
                return INTERVAL
            else:
                self.assets.pop(0)
        print("All previews have been generated !")
        self.save_file()
        self.execute_next_blend()
        return None

    def mark_assets_without_previews(self):
        [asset.asset_mark() for asset in self.assets]
        print(f"Mark {len(self.assets)} assets without previews")
        self.save_file()
        self.execute_next_blend()

    def unmark_assets(self):
        self.assets = [a for a in self.assets if a.asset_data is not None]

        if not self.assets:  # We don't unmark any asset, don't bother saving the file
            print("No asset to unmark")
            return

        for asset in self.assets:
            asset.asset_clear()
            print(f"Unmark {asset.name}")

        self.save_file()
