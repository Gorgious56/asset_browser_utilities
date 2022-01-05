import functools
import os
import numpy as np
from pathlib import Path
import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, PointerProperty
from bpy.types import Operator

from asset_browser_utilities.prop.filter_type import FilterTypes
from asset_browser_utilities.prop.filter_name import FilterName


INTERVAL = 0.2


class ASSET_OT_batch_mark_or_unmark(Operator, ImportHelper):
    bl_idname = "asset.batch_mark_or_unmark"
    bl_label = "Batch Mark or Unmark Assets"

    filter_glob: StringProperty(
        default="",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    this_file_only: BoolProperty(
        default=False,
        name="Act only on this file",
    )

    recursive: BoolProperty(
        default=True,
        name="Recursive",
        description="Operate on blend files located in sub folders recursively\nIf unchecked it will only treat files in this folder",
    )

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

    filter_name: PointerProperty(type=FilterName)

    filter_types: PointerProperty(type=FilterTypes)

    def invoke(self, context, event):
        self.filter_types.initialize()
        if self.this_file_only:
            return context.window_manager.invoke_props_dialog(self)
        else:
            context.window_manager.fileselect_add(self)
            return {"RUNNING_MODAL"}

    def execute(self, context):
        if bpy.data.is_saved and bpy.data.is_dirty:
            bpy.ops.wm.save_mainfile()
        if self.this_file_only:
            blends = [str(bpy.data.filepath)]
        else:
            folder = Path(self.filepath)
            if not folder.is_dir():
                folder = folder.parent
            if self.recursive:
                blends = [fp for fp in folder.glob("**/*.blend") if fp.is_file()]
            else:
                blends = [fp for fp in folder.glob("*.blend") if fp.is_file()]

        settings = {
            "prevent_backup": self.prevent_backup,
            "overwrite": self.overwrite,
            "generate_previews": self.generate_previews,
            "mark": self.mark,
            "filter_name": self.filter_name,
            "filter_types": self.filter_types,
        }

        do_blends(blends, context, settings)

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout

        if not self.this_file_only:
            layout.prop(self, "recursive", icon="FOLDER_REDIRECT")
        layout.prop(self, "prevent_backup", icon="TRASH")
        if self.mark:
            layout.prop(self, "overwrite", icon="ASSET_MANAGER")
            layout.prop(self, "generate_previews", icon="RESTRICT_RENDER_OFF")
        
        self.filter_types.draw(layout)
        self.filter_name.draw(layout)


def do_blends(blends, context, settings, save=None):
    if save is not None:
        bpy.ops.wm.save_as_mainfile(filepath=str(save))
        if settings["prevent_backup"]:
            backup = str(save) + "1"
            if os.path.exists(backup):
                print("Removing backup " + backup)
                os.remove(backup)

    if not blends:
        print("Batch conversion completed")
        return
    print(f"{len(blends)} file{'s' if len(blends) > 1 else ''} left")

    blend = blends.pop(0)
    if bpy.data.filepath != str(blend):
        bpy.ops.wm.open_mainfile(filepath=str(blend))


    do_blends_callback = lambda _save: do_blends(blends, context, settings, save=_save)

    assets = []
    settings["filter_types"].populate(assets)
    settings["filter_name"].filter(assets)

    if settings["mark"]:        
        assets = [a for a in assets if a.asset_data is None or settings["overwrite"]]

        if not assets:  # We don't mark any asset, don't bother saving the file
            print("No asset to mark")
            do_blends_callback(None)
            return

        if settings["generate_previews"]:
            for asset in assets:                
                asset.asset_mark()                
                asset.asset_generate_preview()
                print(f"Mark {asset.name}")
            bpy.app.timers.register(
                functools.partial(
                    sleep_until_previews_are_done, 
                    assets, 
                    lambda: do_blends_callback(blend))
            )  
        else:
            [asset.asset_mark() for asset in assets]
            print(f"Mark {len(assets)} assets without previews")
            do_blends_callback(blend)
                     
    else:  # Unmark assets
        assets = [a for a in assets if a.asset_data is not None]

        if not assets:  # We don't unmark any asset, don't bother saving the file
            print("No asset to unmark")
            do_blends_callback(None)
            return

        for asset in assets:
            asset.asset_clear()
            print(f"Unmark {asset.name}")
        do_blends_callback(blend)


def sleep_until_previews_are_done(assets, callback):
    while assets:  # Check if all previews have been generated
        preview = assets[0].preview
        arr = np.zeros((preview.image_size[0] * preview.image_size[1]) * 4, dtype=np.float32)
        preview.image_pixels_float.foreach_get(arr)
        if np.all((arr == 0)):
            # print(f"Asset preview for {assets[0].name} was not generated. Waiting for {INTERVAL} seconds")
            return INTERVAL
        else:
            # print(f"Asset preview for {assets[0].name} was generated. Removing it from pool")
            assets.pop(0)
    callback()
    return None