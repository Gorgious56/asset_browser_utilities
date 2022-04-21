import bpy


def get_preferences(context):
    return context.preferences.addons["asset_browser_utilities"].preferences


def get_cache(context):
    return get_preferences(context).cache


def write_to_cache(value, context=None):
    if context is None:
        context = bpy.context
    get_cache(context).set(value)


def get_from_cache(_type, context=None):
    if context is None:
        context = bpy.context
    return get_cache(context).get(_type)

class CacheMapping:
    CACHE_MAPPING = ""

    @classmethod
    def get_from_cache(cls, context):
        return getattr(get_cache(context), cls.CACHE_MAPPING)
