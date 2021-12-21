# This is released under CC0 licence. Do with it what you wish. No result guaranteed whatsoever.

bl_info = {
    "name": "Batch Generate Asset Browser Previews ",
    "author": "Gorgious",
    "description": "Batch generate default previews for the Asset Browser from selected folder",
    "blender": (3, 0, 0),
    "version": (0, 0, 2),
    "location": "",
    "warning": "",
    "category": "Import-Export",
}

from pathlib import Path
import bpy
import functools
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator


INTERVAL = 1.0


class ASSET_OT_batch_generate_previews(Operator, ImportHelper):
    bl_idname = "asset.batch_generate_previews"
    bl_label = "Batch Generate Asset Previews"

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
        for filter in ("objects", "materials", "actions", "worlds"):
            if getattr(self, "mark_" + filter):
                mark_filters.append(filter)

        do_blends(blends, mark_filters, generate_previews=self.generate_previews)

        return {"FINISHED"}


def do_blends(blends, mark_filters, generate_previews=True, save=None):
    if save is not None:
        bpy.ops.wm.save_as_mainfile(filepath=str(save))

    if not blends:
        print("Batch conversion completed")
        return
    print(f"{len(blends)} files left")

    blend = blends.pop(0)
    bpy.ops.wm.open_mainfile(filepath=str(blend))

    assets = []
    for filter in mark_filters:
        assets.extend([o for o in getattr(bpy.data, filter)])

    if not generate_previews:
        [asset.asset_mark() for asset in assets]
        do_blends(blends, mark_filters, generate_previews=False, save=blend)
    else:
        bpy.app.timers.register(functools.partial(do_assets, blends, blend, assets, mark_filters))


def message_popup(self, context, messages):
    for message in messages:
        self.layout.label(text=message)


def do_assets(blends, blend, assets, mark_filters):
    if assets:
        asset = assets.pop(0)
        bpy.context.window_manager.popup_menu(
            lambda s, c: message_popup(s, c, (type(asset).__name__, asset.name, f"{len(assets)} to go")),
            title="Asset Marked",
            icon="INFO",
        )
        asset.asset_mark()
        bpy.ops.ed.lib_id_generate_preview({"id": asset})
        return INTERVAL
    do_blends(blends, mark_filters, save=blend)    
    bpy.context.window_manager.popup_menu(
        lambda s, c: message_popup(s, c, ("Done !", )),
        title="Update",
        icon="INFO",
    )
    return None


def menu_func_import(self, context):
    self.layout.operator(ASSET_OT_batch_generate_previews.bl_idname, text=ASSET_OT_batch_generate_previews.bl_label)


def register():
    bpy.utils.register_class(ASSET_OT_batch_generate_previews)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.utils.unregister_class(ASSET_OT_batch_generate_previews)


if __name__ == "__main__":
    register()
