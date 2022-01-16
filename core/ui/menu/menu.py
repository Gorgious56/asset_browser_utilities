import bpy
from bpy.types import Menu
from .prop import FileMenu, LibraryMenu


class ABU_MT_library(Menu, LibraryMenu):
    bl_idname = "ABU_MT_library"
    bl_label = "External Library"

    def draw(self, context):
        layout = self.layout
        draw_shared_menus(layout, "library")


class ABU_MT_this_file(Menu, FileMenu):
    bl_idname = "ABU_MT_this_file"
    bl_label = "Current File"

    LIBRARY = False

    def draw(self, context):
        layout = self.layout
        if bpy.data.is_saved:
            export_op = layout.operator("asset.export", text="Export", icon="EXPORT")
            draw_shared_menus(layout, "file")
        else:
            layout.label(text="Save this file to disk to enable operations", icon="QUESTION")


def draw_shared_menus(layout, infix):
    layout.menu(f"ABU_MT_{infix}_mark", icon="ASSET_MANAGER")
    layout.menu(f"ABU_MT_{infix}_tags", icon="MOD_TINT")
    layout.menu(f"ABU_MT_{infix}_previews", icon="SEQ_PREVIEW")


class ABU_MT_menu(Menu):
    bl_idname = "ABU_MT_menu"
    bl_label = "Batch Operations"

    def draw(self, context):
        layout = self.layout
        layout.menu("ABU_MT_this_file")
        layout.menu("ABU_MT_library")


def menu_draw(self, context):
    self.layout.menu("ABU_MT_menu")


def register():
    bpy.types.ASSETBROWSER_MT_editor_menus.append(menu_draw)


def unregister():
    bpy.types.ASSETBROWSER_MT_editor_menus.remove(menu_draw)
