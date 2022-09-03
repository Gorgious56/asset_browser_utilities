import bpy


def draw_asset_browser_context_menu_appends(self, context):
    layout = self.layout
    layout.operator("abu.open_asset_folder")


def register():
    bpy.types.ASSETBROWSER_MT_context_menu.append(draw_asset_browser_context_menu_appends)


def unregister():
    bpy.types.ASSETBROWSER_MT_context_menu.remove(draw_asset_browser_context_menu_appends)
