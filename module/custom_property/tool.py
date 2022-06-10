def get_prop(obj, name, ensure=True):
    if ensure:
        obj.id_properties_ensure()
    return obj.id_properties_ui(name)


def copy_prop(source, target, name, ensure=True):
    if ensure:
        target.id_properties_ensure()
        source.id_properties_ensure()
    try:
        prop_data_source = get_prop(source, name, ensure=False)
    except TypeError:
        return
    target[name] = source[name]
    prop_data_target = get_prop(target, name, ensure=False)
    prop_data_target.update_from(prop_data_source)
    prop_name_custom = f'["{name}"]'
    target.property_overridable_library_set(prop_name_custom, source.is_property_overridable_library(prop_name_custom))
