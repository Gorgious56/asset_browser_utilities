import bpy

def get_preferences():
    return bpy.context.preferences.addons["asset_browser_utilities"].preferences
