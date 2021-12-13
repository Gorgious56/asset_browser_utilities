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

    def execute(self, context):
        folder = Path(self.filepath)
        if not folder.is_dir():
            folder = folder.parent
        if self.recursive:
            blends = [fp for fp in folder.glob("**/*.blend") if fp.is_file()]
        else:
            blends = [fp for fp in folder.glob("*.blend") if fp.is_file()]
        do_blends(blends)

        return {"FINISHED"}


def do_blends(blends, save=None):
    if save is not None:
        bpy.ops.wm.save_as_mainfile(filepath=str(save))

    if not blends:
        print("Batch conversion completed")
        return
    print(f"{len(blends)} files left")

    blend = blends.pop(0)
    bpy.ops.wm.open_mainfile(filepath=str(blend))

    bpy.app.timers.register(functools.partial(do_objs, blends, blend, [o for o in bpy.data.objects]))

def do_objs(blends, blend, objs):
    if objs:
        obj = objs.pop(0)
        obj.asset_mark()
        bpy.ops.ed.lib_id_generate_preview({"id": obj})
        return INTERVAL
    do_blends(blends, blend)
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
