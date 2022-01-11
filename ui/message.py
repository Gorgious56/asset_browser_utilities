import bpy

# Inspired by https://github.com/LJ3D/AssetLibraryTools - LJ3D


def message_box(message="", title="Info", icon="INFO", context=None):
    def draw(self, context):
        self.layout.label(text=message)

    if context is None:
        bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)
    else:
        context.window_manager.popup_menu(draw, title=title, icon=icon)
