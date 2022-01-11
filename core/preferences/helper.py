import bpy


def get_preferences(context):
    return context.preferences.addons["asset_browser_utilities"].preferences


def write_to_cache(value, context=None):
    if context is None:
        context = bpy.context
    prefs = get_preferences(context)
    prefs.cache_operator.set(value)


def get_from_cache(_type, context=None):
    if context is None:
        context = bpy.context
    prefs = get_preferences(context)
    return prefs.cache_operator.get(_type)
