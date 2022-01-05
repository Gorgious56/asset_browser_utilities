import functools
from pathlib import Path
import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator
import os
import numpy as np

INTERVAL = 0.2


class ASSET_OT_batch_mark_or_unmark(Operator, ImportHelper):
    bl_idname = "asset.batch_mark_or_unmark"
    bl_label = "Batch Mark or Unmark Assets"

    filter_glob: StringProperty(
        default="",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    this_file_only: bpy.props.BoolProperty(
        default=False,
        name="Act only on this file",
    )

    recursive: bpy.props.BoolProperty(
        default=True,
        name="Recursive",
        description="Operate on blend files located in sub folders recursively\nIf unchecked it will only treat files in this folder",
    )

    prevent_backup: bpy.props.BoolProperty(
        name="Remove Backup",
        description="Check to automatically delete the creation of backup files when 'Save Versions' is enabled in the preferences\nThis will prevent duplicating files when they are overwritten\nWarning : Backup files ending in .blend1 will be deleted permantently",
        default=True,
    )

    overwrite: bpy.props.BoolProperty(
        name="Overwrite assets",
        description="Check to re-mark assets and re-generate preview if the item is already an asset",
        default=False,
    )

    mark: bpy.props.BoolProperty(
        name="Mark",
        description="Check to Mark existing assets rather than unmarking items",
        default=False,
    )

    generate_previews: bpy.props.BoolProperty(
        default=True,
        name="Generate Previews",
        description="When marking assets, automatically generate a preview\nUncheck to mark assets really fast",
    )

    filter_name_by: bpy.props.EnumProperty(
        name="Filter Name By",
        items=(
            ("Prefix",) * 3,
            ("Contains",) * 3,
            ("Suffix",) * 3,
        ),
        default="Contains",
    )

    filter_name_value: bpy.props.StringProperty(name="Name Filter Value", description="Filter assets by name\nLeave empty for no filter")

    mark_objects: bpy.props.BoolProperty(default=True, name="Mark Objects")
    mark_materials: bpy.props.BoolProperty(default=False, name="Mark Materials")
    mark_actions: bpy.props.BoolProperty(default=False, name="Mark Actions")
    mark_worlds: bpy.props.BoolProperty(default=False, name="Mark Worlds")

    def invoke(self, context, event):
        if self.this_file_only:
            return context.window_manager.invoke_props_dialog(self)
        else:
            context.window_manager.fileselect_add(self)
            return {"RUNNING_MODAL"}

    def execute(self, context):
        if bpy.data.is_saved:
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

        mark_filters = []
        for a_filter in ("objects", "materials", "actions", "worlds"):
            if getattr(self, "mark_" + a_filter):
                mark_filters.append(a_filter)

        do_blends(
            blends,
            context,
            mark_filters,
            {
                "prevent_backup": self.prevent_backup,
                "overwrite": self.overwrite,
                "generate_previews": self.generate_previews,
                "mark": self.mark,
                "filter_name_by": self.filter_name_by,
                "filter_name_value": self.filter_name_value,
            },
        )

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout

        if not self.this_file_only:
            layout.prop(self, "recursive", icon="FOLDER_REDIRECT")
        layout.prop(self, "prevent_backup", icon="TRASH")
        if self.mark:
            layout.prop(self, "overwrite", icon="ASSET_MANAGER")
            layout.prop(self, "generate_previews", icon="RESTRICT_RENDER_OFF")

        box = layout.box()
        box.label(text="Filter By Type")
        col = box.column(align=True)
        col.prop(self, "mark_actions", text="Actions", icon="ACTION")
        col.prop(self, "mark_materials", text="Materials", icon="MATERIAL")
        col.prop(self, "mark_objects", text="Objects", icon="OBJECT_DATA")
        col.prop(self, "mark_worlds", text="Worlds", icon="WORLD")

        box = layout.box()
        box.label(text="Filter By Name")
        box.prop(self, "filter_name_value", text="Text")
        row = box.row(align=True)
        row.props_enum(self, "filter_name_by")


def do_blends(blends, context, mark_filters, settings, save=None):
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
    print(f"{len(blends)} files left")

    blend = blends.pop(0)
    bpy.ops.wm.open_mainfile(filepath=str(blend))

    assets = []
    if settings["mark"]:
        filter_name_value = settings["filter_name_value"]
        filter_name_by = settings["filter_name_by"]
        for a_filter in mark_filters:
            for o in getattr(bpy.data, a_filter):
                if filter_name_value != "":
                    if filter_name_by == "Prefix":
                        if not o.name.startswith(filter_name_value):
                            continue
                    elif filter_name_by == "Contains":
                        if not filter_name_value in o.name:
                            continue
                    elif filter_name_by == "Suffix":
                        if not o.name.endswith(filter_name_value):
                            continue
                if o.asset_data is None or settings["overwrite"]:
                    assets.append(o)
        if not assets:  # We don't mark any assets, so don't bother saving the file
            print("No asset to mark")
            do_blends(blends, context, mark_filters, settings, save=None)
            return

        if not settings["generate_previews"]:
            [asset.asset_mark() for asset in assets]
            do_blends(blends, context, mark_filters, settings, save=blend)
        else:
            bpy.app.timers.register(
                functools.partial(do_assets, context, blends, blend, assets, mark_filters, settings)
            )
    else:
        for a_filter in mark_filters:
            assets.extend([o for o in getattr(bpy.data, a_filter) if o.asset_data])
        [asset.asset_clear() for asset in assets]
        do_blends(blends, context, mark_filters, settings, save=blend)


def do_assets(context, blends, blend, assets, mark_filters, settings):
    last_asset = do_assets.last_asset
    if last_asset is not None:
        # Check if the last preview has successfully generated
        preview = last_asset.preview
        arr = np.zeros((preview.image_size[0] * preview.image_size[1]) * 4, dtype=np.float32)
        preview.image_pixels_float.foreach_get(arr)
        if np.all((arr == 0)):
            # print(f"Asset preview was not generated. Waiting for {INTERVAL * do_assets.last_check} seconds")
            do_assets.last_check += 1
            return INTERVAL * do_assets.last_check
        else:
            do_assets.last_asset = None
            do_assets.last_check = 1
    if assets:
        asset = assets.pop(0)
        asset.asset_mark()
        asset.asset_generate_preview()
        do_assets.last_asset = asset
        return INTERVAL
    do_blends(blends, context, mark_filters, settings, save=blend)
    return None


do_assets.last_asset = None
do_assets.last_check = 1
