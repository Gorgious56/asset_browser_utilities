import functools
from pathlib import Path
import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator
import os

INTERVAL = 1.0


class ASSET_OT_batch_mark(Operator, ImportHelper):
    bl_idname = "asset.batch_mark"
    bl_label = "Batch Mark Assets"

    filter_glob: StringProperty(
        default="",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    recursive: bpy.props.BoolProperty(
        default=True,
        name="Recursive",
        description="Operate on blend files located in sub folders recursively\nIf unchecked it will only treat files in this folder",
    )

    prevent_backup: bpy.props.BoolProperty(
        name="Remove Backup",
        description="Check to automatically delete the creation of backup files when 'Save Versions' is enabled in the preferences\nThis will prevent duplicating files when they are overwritten\nWarning : Backup files will be deleted permantently",
        default=False,
    )

    overwrite: bpy.props.BoolProperty(
        name="Overwrite assets",
        description="Check to re-mark assets and re-generate preview if the item is already an asset",
        default=False,
    )

    unmark: bpy.props.BoolProperty(
        name="Unmark",
        description="Check to unmark existing assets rather than marking items",
        default=False,
    )

    generate_previews: bpy.props.BoolProperty(
        default=True,
        name="Generate Previews",
        description="When marking assets, automatically generate a preview\nUncheck to mark assets really fast",
    )

    mark_objects: bpy.props.BoolProperty(default=True, name="Mark Objects")
    mark_materials: bpy.props.BoolProperty(default=False, name="Mark Materials")
    mark_actions: bpy.props.BoolProperty(default=False, name="Mark Actions")
    mark_worlds: bpy.props.BoolProperty(default=False, name="Mark Worlds")

    def execute(self, context):
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
                "unmark": self.unmark,
            },
        )

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "recursive", icon="FOLDER_REDIRECT")
        layout.prop(self, "prevent_backup", icon="TRASH")
        layout.prop(self, "overwrite", icon="ASSET_MANAGER")
        layout.prop(self, "generate_previews", icon="RESTRICT_RENDER_OFF")

        box = layout.box()
        box.label(text="Mark :")
        col = box.column(align=True)
        col.prop(self, "mark_actions", text="Actions", icon="ACTION")
        col.prop(self, "mark_materials", text="Materials", icon="MATERIAL")
        col.prop(self, "mark_objects", text="Objects", icon="OBJECT_DATA")
        col.prop(self, "mark_worlds", text="Worlds", icon="WORLD")

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
    if settings["unmark"]:
        for a_filter in mark_filters:
            assets.extend([o for o in getattr(bpy.data, a_filter) if o.asset_data])
        [asset.asset_clear() for asset in assets]
        do_blends(blends, context, mark_filters, settings, save=blend)
    else:
        for a_filter in mark_filters:
            assets.extend([o for o in getattr(bpy.data, a_filter) if o.asset_data is None or settings["overwrite"]])
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


def do_assets(context, blends, blend, assets, mark_filters, settings):
    if assets:
        asset = assets.pop(0)
        asset.asset_mark()
        asset.asset_generate_preview()
        return INTERVAL
    do_blends(blends, context, mark_filters, settings, save=blend)
    return None
