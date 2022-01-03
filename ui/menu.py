import bpy
from bpy_extras.asset_utils import SpaceAssetInfo


class BGABP_MT_menu(bpy.types.Menu):
    bl_idname = "BGABP_MT_menu"
    bl_label = "Batch Operations"

    @classmethod
    def poll(cls, context):
        return SpaceAssetInfo.is_asset_browser_poll(context)

    def draw(self, _context):
        layout = self.layout

        mark_op = layout.operator("asset.batch_mark", text="Mark Assets")
        mark_op.unmark = False
        unmark_op = layout.operator("asset.batch_mark", text="Unmark Assets")
        unmark_op.unmark = True


def menu_draw(self, context):
    self.layout.menu("BGABP_MT_menu")


def register():
    bpy.types.ASSETBROWSER_MT_editor_menus.append(menu_draw)


def unregister():
    bpy.types.ASSETBROWSER_MT_editor_menus.remove(menu_draw)
