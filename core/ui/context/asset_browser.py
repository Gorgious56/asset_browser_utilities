import bpy


def draw_outliner_context_menu_appends(self, context):
    layout = self.layout
    layout.operator("abu.open_linked_object_blend_file", icon="LINKED")
    

def draw_asset_browser_context_menu_appends(self, context):
    layout = self.layout
    layout.operator("abu.open_asset_folder")
    # layout.operator("abu.linked_users")


def register():
    bpy.types.ASSETBROWSER_MT_context_menu.append(draw_asset_browser_context_menu_appends)
    bpy.types.OUTLINER_MT_asset.append(draw_outliner_context_menu_appends)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_outliner_context_menu_appends)


def unregister():
    bpy.types.ASSETBROWSER_MT_context_menu.remove(draw_asset_browser_context_menu_appends)
    bpy.types.OUTLINER_MT_asset.remove(draw_outliner_context_menu_appends)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_outliner_context_menu_appends)
