# This is released under CC0 licence. Do with it what you wish. No result guaranteed whatsoever.

bl_info = {
    "name": "Batch Generate Asset Browser Previews ",
    "author": "Gorgious",
    "description": "Batch generate default previews for the Asset Browser from selected files",
    "blender": (3, 0, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Import-Export",
}

import pathlib
import bpy
import functools
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator


class ASSET_OT_batch_generate_previews(Operator, ImportHelper):
    bl_idname = "asset.batch_generate_previews"
    bl_label = "Batch Generate Asset Previews"

    filter_glob: StringProperty(
        default="",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        p = pathlib.Path(str(os.path.dirname(self.filepath)))
        blends = [fp for fp in p.glob("**/*.blend") if fp.is_file()]
        bpy.app.timers.register(functools.partial(in_x_seconds, blends), first_interval=2.0)

        return {"FINISHED"}


def in_x_seconds(blends, save=None):
    if save is not None:
        bpy.ops.wm.save_as_mainfile(filepath=str(save))

    if not blends:
        print("Batch conversion completed")
        return

    blend = blends.pop(0)
    bpy.ops.wm.open_mainfile(filepath=str(blend))

    for obj in bpy.data.objects:
        obj.asset_mark()
        bpy.ops.ed.lib_id_generate_preview({"id": obj})

    bpy.app.timers.register(functools.partial(in_x_seconds, blends, blend), first_interval=2.0)
    print(f"{len(blends)} files left")


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
