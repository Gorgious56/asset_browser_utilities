import re


def remove_trailing_numbers(obj, prop_name):
    name = getattr(obj, prop_name)
    search = re.search("\.[0-9]+$", name)
    if search:
        setattr(obj, prop_name, name[0 : search.start()])


def rename(obj, mode, value, remove_trailing):
    if remove_trailing:
        remove_trailing_numbers(obj, "name")
    if mode == "Prefix":
        obj.name = value + obj.name
    elif mode == "Replace":
        obj.name = value
    elif mode == "Suffix":
        obj.name = obj.name + value


class RenameAssetOperation:
    MAPPING = "RENAME_ASSET"
    LABEL = "Rename Asset"
    DESCRIPTION = "Rename Asset"
    OPERATION = lambda assets, mode, value, : [rename(a, mode, value, False) for a in assets]
    ATTRIBUTES = ("enum_value", "string_value")
    ATTRIBUTES_NAMES = ("Mode", None)

    @staticmethod
    def get_enum_items():
        return (("Prefix",) * 3, ("Replace",) * 3, ("Suffix",) * 3)
