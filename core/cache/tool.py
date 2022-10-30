from asset_browser_utilities.core.preferences.tool import get_preferences


def get_cache():
    return get_preferences().cache


def get_from_cache(cls):
    return get_cache().get(cls)

def get_current_operator_properties():
    cache = get_cache()
    for prop_name in cache.__annotations__:
        prop = getattr(cache, prop_name)
        if str(prop.__class__) == cache.op_current.class_name:
            return prop


def get_presets(op, context):
    # First entry is the default preset
    enum = [("ABU_DEFAULT", "Default", "Use default values (defined in Addon Preferences)")]
    for preset in get_preferences().presets:
        enum.append((preset.name,) * 3)
    return enum
