import bpy


class AssetBrowserMenu:
    # from space_filebrowser.py
    @classmethod
    def poll(cls, context):
        from bpy_extras.asset_utils import SpaceAssetInfo

        return SpaceAssetInfo.is_asset_browser_poll(context)


class ABUMenu:
    def draw_mark_or_unmark(self, layout, this_file_only):        
        mark_op = layout.operator("asset.batch_mark", text="Mark Assets", icon="ASSET_MANAGER")
        mark_op.library_export_settings.this_file_only = this_file_only
        unmark_op = layout.operator("asset.batch_unmark", text="Unmark Assets", icon="ASSET_MANAGER")
        unmark_op.library_export_settings.this_file_only = this_file_only

    def draw_tags_add_or_remove(self, layout, this_file_only):
        add_tags_op = layout.operator("asset.tags_add_or_remove", text="Add Tags", icon="MOD_TINT")
        add_tags_op.library_export_settings.this_file_only = this_file_only
        add_tags_op.tag_collection.add = True
        remove_tags_op = layout.operator("asset.tags_add_or_remove", text="Remove Tags", icon="MOD_TINT")
        remove_tags_op.library_export_settings.this_file_only = this_file_only
        remove_tags_op.tag_collection.add = False


class ABU_MT_library(AssetBrowserMenu, bpy.types.Menu, ABUMenu):
    bl_idname = "ABU_MT_library"
    bl_label = "External Library"

    def draw(self, context):
        layout = self.layout
        self.draw_mark_or_unmark(layout, this_file_only=False)
        self.draw_tags_add_or_remove(layout, this_file_only=False)


class ABU_MT_this_file(AssetBrowserMenu, bpy.types.Menu, ABUMenu):
    bl_idname = "ABU_MT_this_file"
    bl_label = "This File"

    def draw(self, context):
        layout = self.layout
        if bpy.data.is_saved:
            self.draw_mark_or_unmark(layout, this_file_only=True)
            self.draw_tags_add_or_remove(layout, this_file_only=True)
            
            export_op = layout.operator("asset.export", text="Export", icon="EXPORT")
            load_previews_from_disk = layout.operator("asset.load_previews_from_disk", text="Load Previews From Disk", icon="SEQ_PREVIEW")
            
        else:
            layout.label(text="Save this file to disk to enable operations", icon="QUESTION")


class ABU_MT_menu(AssetBrowserMenu, bpy.types.Menu):
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
