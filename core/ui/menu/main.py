from asset_browser_utilities.core.preferences.helper import get_preferences
import bpy
from bpy.types import Menu
from .helper import set_layout_library, is_library


class ABU_MT_submenu(Menu):
    bl_idname = "ABU_MT_submenu"
    bl_label = "External Library"

    def draw(self, context):
        layout = self.layout
        if is_library(context):
            self.draw_shared_menus()
        else:
            if bpy.data.is_saved:
                export_op = layout.operator("asset.export", text="Export", icon="EXPORT")
                self.draw_shared_menus()
            else:
                layout.label(text="Save this file to disk to enable operations", icon="QUESTION")


    def draw_shared_menus(self):
        layout = self.layout
        layout.menu("ABU_MT_assets", icon="ASSET_MANAGER")
        layout.menu("ABU_MT_tags", icon="BOOKMARKS")
        layout.menu("ABU_MT_previews", icon="SEQ_PREVIEW")
        layout.menu("ABU_MT_catalogs", icon="OUTLINER_COLLECTION")
        layout.menu("ABU_MT_author", icon="USER")
        layout.menu("ABU_MT_description", icon="FILE_TEXT")


class ABU_MT_menu(Menu):
    bl_idname = "ABU_MT_menu"
    bl_label = "Batch Operations"

    def draw(self, context):
        layout = self.layout
        layout.menu("ABU_MT_submenu", text="Current File")
        set_layout_library(layout)
        layout.menu("ABU_MT_submenu", text="External Library")


def menu_draw(self, context):
    self.layout.menu("ABU_MT_menu")


def register():
    bpy.types.ASSETBROWSER_MT_editor_menus.append(menu_draw)


def unregister():
    bpy.types.ASSETBROWSER_MT_editor_menus.remove(menu_draw)
