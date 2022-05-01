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


def get_enum_items():
    return (("Prefix",) * 3, ("Replace",) * 3, ("Suffix",) * 3)


class RenameAssetOperation:
    MAPPING = "RENAME_ASSET"
    LABEL = "Rename Asset"
    DESCRIPTION = "Rename Asset"
    OPERATION = lambda assets, mode, value: [rename(a, mode, value, False) for a in assets]
    ATTRIBUTES = ("enum_value", "string_value")
    ATTRIBUTES_NAMES = ("Mode", None)

    @staticmethod
    def get_enum_items():
        return get_enum_items()


class RenameDataOperation:
    MAPPING = "RENAME_DATA"
    LABEL = "Rename Data"
    DESCRIPTION = "Rename Data"
    OPERATION = lambda assets, mode, value, same_as_asset: [
        rename(
            a.data,
            "Replace" if same_as_asset else mode,
            a.name if same_as_asset else value,
            False,
        )
        for a in assets
        if hasattr(a, "data") and a.data is not None
    ]
    ATTRIBUTES = ("enum_value", "string_value", "bool_value")

    @staticmethod
    def get_enum_items():
        return get_enum_items()

    @staticmethod
    def draw(layout, operation_pg):
        layout.prop(operation_pg, "bool_value", text="Same as Asset ?")
        if not operation_pg.bool_value:
            layout.prop(operation_pg, "enum_value", text="Mode")
            layout.prop(operation_pg, "string_value")
