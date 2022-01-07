import bpy


class AssetBrowserMenu:
    # from space_filebrowser.py
    @classmethod
    def poll(cls, context):
        from bpy_extras.asset_utils import SpaceAssetInfo

        return SpaceAssetInfo.is_asset_browser_poll(context)


class BGABP_MT_library(AssetBrowserMenu, bpy.types.Menu):
    bl_idname = "BGABP_MT_library"
    bl_label = "External Library"

    def draw(self, context):
        layout = self.layout

        mark_op = layout.operator("asset.batch_mark_or_unmark", text="Mark Assets")
        mark_op.library_export_settings.this_file_only = False
        mark_op.mark = True

        unmark_op = layout.operator("asset.batch_mark_or_unmark", text="Unmark Assets")
        unmark_op.library_export_settings.this_file_only = False
        unmark_op.mark = False


class BGABP_MT_this_file(AssetBrowserMenu, bpy.types.Menu):
    bl_idname = "BGABP_MT_this_file"
    bl_label = "This File"

    def draw(self, context):
        layout = self.layout
        if bpy.data.is_saved:
            mark_op = layout.operator("asset.batch_mark_or_unmark", text="Mark Assets")
            mark_op.library_export_settings.this_file_only = True
            mark_op.mark = True

            unmark_op = layout.operator("asset.batch_mark_or_unmark", text="Unmark Assets")
            unmark_op.library_export_settings.this_file_only = True
            unmark_op.mark = False
            
            export_op = layout.operator("asset.export", text="Export Assets")
        else:
            layout.label(text="Save this file to disk to enable marking assets", icon="QUESTION")


class BGABP_MT_menu(AssetBrowserMenu, bpy.types.Menu):
    bl_idname = "BGABP_MT_menu"
    bl_label = "Batch Operations"

    def draw(self, context):
        layout = self.layout
        layout.menu("BGABP_MT_this_file")
        layout.menu("BGABP_MT_library")


def menu_draw(self, context):
    self.layout.menu("BGABP_MT_menu")


def register():
    bpy.types.ASSETBROWSER_MT_editor_menus.append(menu_draw)


def unregister():
    bpy.types.ASSETBROWSER_MT_editor_menus.remove(menu_draw)
