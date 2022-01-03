import bpy
from bpy_extras.asset_utils import SpaceAssetInfo


class BGABP_MT_menu(bpy.types.Menu):
    bl_idname = "BGABP_MT_menu"
    bl_label = "Batch Operations"

    @classmethod
    def poll(cls, context):
        return SpaceAssetInfo.is_asset_browser_poll(context)

    def draw(self, context):
        layout = self.layout

        mark_op = layout.operator("asset.batch_mark_or_unmark", text="Mark Assets in External Library")
        mark_op.this_file_only = False
        mark_op.mark = True

        unmark_op = layout.operator("asset.batch_mark_or_unmark", text="Unmark Assets in External Library")
        unmark_op.this_file_only = False
        unmark_op.mark = False

        if bpy.data.is_saved:
            mark_op = layout.operator("asset.batch_mark_or_unmark", text="Mark Assets in this File")
            mark_op.this_file_only = True
            mark_op.mark = True

            unmark_op = layout.operator("asset.batch_mark_or_unmark", text="Unmark Assets in this File")
            unmark_op.this_file_only = True
            unmark_op.mark = False
        else:
            layout.label(text="Make sure to save this file to enable marking assets", icon="QUESTION")


def menu_draw(self, context):
    self.layout.menu("BGABP_MT_menu")


def register():
    bpy.types.ASSETBROWSER_MT_editor_menus.append(menu_draw)


def unregister():
    bpy.types.ASSETBROWSER_MT_editor_menus.remove(menu_draw)
