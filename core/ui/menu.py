import bpy
from bpy.types import Menu


class AssetBrowserMenu:
    # from space_filebrowser.py
    @classmethod
    def poll(cls, context):
        from bpy_extras.asset_utils import SpaceAssetInfo

        return SpaceAssetInfo.is_asset_browser_poll(context)


class LibraryMenu:
    LIBRARY = True


class FileMenu:
    LIBRARY = False


class ABUMenu:
    def draw_mark_or_unmark(self):
        mark_op = self.layout.operator("asset.batch_mark", text="Mark Assets", icon="ASSET_MANAGER")
        mark_op.library_settings.this_file_only = not self.LIBRARY
        unmark_op = self.layout.operator("asset.batch_unmark", text="Unmark Assets", icon="ASSET_MANAGER")
        unmark_op.library_settings.this_file_only = not self.LIBRARY

    def draw_previews(self):
        self.draw_batch_generate_previews()
        self.layout.operator("asset.load_previews_from_disk", text="Load From Disk", icon="IMPORT")

    def draw_batch_generate_previews(self):
        op = self.layout.operator("asset.batch_generate_previews", text="Batch Generate", icon="FILE_REFRESH")
        op.library_settings.this_file_only = not self.LIBRARY

    def draw_tags(self):
        add_tags_op = self.layout.operator("asset.batch_add_tags", text="Batch Add", icon="ADD")
        add_tags_op.library_settings.this_file_only = not self.LIBRARY
        remove_tags_op = self.layout.operator("asset.batch_remove_tags", text="Batch Remove", icon="REMOVE")
        remove_tags_op.library_settings.this_file_only = not self.LIBRARY


class ABU_MT_library_tags(Menu, ABUMenu, LibraryMenu):
    bl_label = "Tags"

    def draw(self, context):
        self.draw_tags()


class ABU_MT_file_tags(Menu, ABUMenu, FileMenu):
    bl_label = "Tags"

    def draw(self, context):
        self.draw_tags()


class ABU_MT_library_previews(Menu, ABUMenu, LibraryMenu):
    bl_label = "Previews"

    def draw(self, context):
        self.draw_previews()


class ABU_MT_file_previews(Menu, ABUMenu, FileMenu):
    bl_label = "Previews"

    def draw(self, context):
        self.draw_previews()


class ABU_MT_library(AssetBrowserMenu, Menu, ABUMenu, LibraryMenu):
    bl_idname = "ABU_MT_library"
    bl_label = "External Library"

    def draw(self, context):
        layout = self.layout
        self.draw_mark_or_unmark()
        layout.menu("ABU_MT_library_tags", icon="MOD_TINT")
        layout.menu("ABU_MT_library_previews", icon="SEQ_PREVIEW")


class ABU_MT_this_file(AssetBrowserMenu, Menu, ABUMenu, FileMenu):
    bl_idname = "ABU_MT_this_file"
    bl_label = "This File"

    LIBRARY = False

    def draw(self, context):
        layout = self.layout
        if bpy.data.is_saved:
            self.draw_mark_or_unmark()

            export_op = layout.operator("asset.export", text="Export", icon="EXPORT")
            layout.menu("ABU_MT_file_tags", icon="MOD_TINT")
            layout.menu("ABU_MT_file_previews", icon="SEQ_PREVIEW")

        else:
            layout.label(text="Save this file to disk to enable operations", icon="QUESTION")


class ABU_MT_menu(AssetBrowserMenu, Menu):
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
