def copy_simple_property_group(source, target):
    for prop_name in source.__annotations__.keys():
        try:
            setattr(target, prop_name, getattr(source, prop_name))
        except AttributeError:
            pass
