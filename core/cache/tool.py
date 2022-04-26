from asset_browser_utilities.core.preferences.tool import get_preferences
import bpy


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


def get_presets(op, context):
    # First entry is the default preset
    enum = [("ABU_DEFAULT", "Default", "Use default values (defined in Addon Preferences)")]
    for preset in get_preferences(context).presets:
        enum.append((preset.name,) * 3)
    return enum


class CacheMapping:
    CACHE_MAPPING = ""

    @classmethod
    def get_from_cache(cls, context):
        return getattr(get_cache(context), cls.CACHE_MAPPING)
