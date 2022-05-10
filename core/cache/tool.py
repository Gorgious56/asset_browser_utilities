from asset_browser_utilities.core.preferences.tool import get_preferences


def get_cache():
    return get_preferences().cache


def write_to_cache(value):
    get_cache().set(value)


def get_from_cache(_type):
    return get_cache().get(_type)


def get_presets(op, context):
    # First entry is the default preset
    enum = [("ABU_DEFAULT", "Default", "Use default values (defined in Addon Preferences)")]
    for preset in get_preferences().presets:
        enum.append((preset.name,) * 3)
    return enum


class CacheMapping:
    CACHE_MAPPING = ""

    @classmethod
    def get_from_cache(cls):
        return getattr(get_cache(), cls.CACHE_MAPPING)
