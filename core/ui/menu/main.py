from asset_browser_utilities.core.preferences.helper import get_preferences
import bpy
from bpy.types import Menu
from .helper import is_library_user, set_layout_library, is_library, set_layout_library_user


class ABU_MT_submenu(Menu):
    bl_idname = "ABU_MT_submenu"
    bl_label = ""

    def draw(self, context):
        if bpy.data.is_saved or is_library(context):
            if is_library_user(context) and not context.preferences.filepaths.asset_libraries:
                self.layout.label(text="Add User Library in Edit > Preferences > File Paths", icon="QUESTION")
            else:
                self.draw_shared_menus(context)
        else:
            self.layout.label(text="Save this file to disk to enable operations", icon="QUESTION")

    def draw_shared_menus(self, context):
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
        layout.menu("ABU_MT_submenu", text="External File/Folder")
        set_layout_library_user(layout)
        layout.menu("ABU_MT_submenu", text="User Library")


def menu_draw(self, context):
    self.layout.menu("ABU_MT_menu")


def register():
    bpy.types.ASSETBROWSER_MT_editor_menus.append(menu_draw)


def unregister():
    bpy.types.ASSETBROWSER_MT_editor_menus.remove(menu_draw)
