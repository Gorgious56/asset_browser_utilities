import bpy
from bpy.types import Menu

from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.cache.tool import get_current_operator_properties

from .tool import set_layout_library_file_external, set_layout_library_folder, set_layout_library_user


class ABU_MT_submenu(Menu):
    bl_idname = "ABU_MT_submenu"
    bl_label = ""

    def draw(self, context):
        if (
            LibraryType.get_library_type_from_context(context) == LibraryType.UserLibrary.value
            and not context.preferences.filepaths.asset_libraries
        ):
            self.layout.label(text="Add User Library in Edit > Preferences > File Paths", icon="QUESTION")
        elif (
            LibraryType.get_library_type_from_context(context) == LibraryType.FileCurrent.value
            and not bpy.data.is_saved
        ):
            self.layout.label(text="Save File to disk to enable operations", icon="QUESTION")
        else:
            self.draw_shared_menus(context)

    def draw_shared_menus(self, context):
        layout = self.layout
        layout.menu("ABU_MT_assets", icon="ASSET_MANAGER")
        layout.menu("ABU_MT_tags", icon="BOOKMARKS")
        layout.menu("ABU_MT_custom_properties", icon="PROPERTIES")
        layout.menu("ABU_MT_previews", icon="SEQ_PREVIEW")
        layout.menu("ABU_MT_catalogs", icon="OUTLINER_COLLECTION")
        layout.menu("ABU_MT_author", icon="USER")
        layout.menu("ABU_MT_copyright", icon="COPY_ID")
        layout.menu("ABU_MT_description", icon="FILE_TEXT")
        layout.menu("ABU_MT_license", icon="FAKE_USER_OFF")
        layout.menu("ABU_MT_material", icon="MATERIAL")
        layout.menu("ABU_MT_node_tree", icon="NODETREE")
        if LibraryType.get_library_type_from_context(context) == LibraryType.UserLibrary.value:
            layout.menu("ABU_MT_blend", icon="BLENDER")
        if LibraryType.get_library_type_from_context(context) in (
            LibraryType.FolderExternal.value,
            LibraryType.UserLibrary.value,
        ):
            layout.menu("ABU_MT_convert", icon="MESH_MONKEY")


class ABU_MT_menu(Menu):
    bl_idname = "ABU_MT_menu"
    bl_label = "Batch Operations"

    def draw(self, context):
        layout = self.layout
        layout.menu("ABU_MT_submenu", text="Current File", icon="FILE_BLEND")
        set_layout_library_file_external(layout)
        layout.menu("ABU_MT_submenu", text="External File(s)", icon="FILE")
        set_layout_library_folder(layout)
        layout.menu("ABU_MT_submenu", text="External Folder", icon="FILE_FOLDER")
        set_layout_library_user(layout)
        layout.menu("ABU_MT_submenu", text="User Library", icon="ASSET_MANAGER")


def menu_draw(self, context):
    progress_props = context.window_manager.abu_progress
    factor = progress_props.factor
    if 0 <= factor < 1:
        row = self.layout.row()
        row.scale_x = 5
        row.progress(
            factor=factor,
            type="BAR",
            text=f"{get_current_operator_properties().__class__.__name__.replace('OperatorProperties', '')} ({progress_props.tasks_current}/{progress_props.tasks_total})",
        )
    else:
        self.layout.menu("ABU_MT_menu")


def register():
    bpy.types.ASSETBROWSER_MT_editor_menus.append(menu_draw)


def unregister():
    bpy.types.ASSETBROWSER_MT_editor_menus.remove(menu_draw)
