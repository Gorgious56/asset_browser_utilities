import re
from pathlib import Path
from asset_browser_utilities.core.operator.prop import ObjectFilteredOperation
import bpy


def remove_trailing_numbers(obj, prop_name):
    name = getattr(obj, prop_name)
    search = re.search("\.[0-9]+$", name)
    if search:
        setattr(obj, prop_name, name[0 : search.start()])


def rename(obj, mode, value, value_from, remove_trailing):
    "obj can be any object that has 'name' as an attribute"
    if remove_trailing:
        remove_trailing_numbers(obj, "name")
    if mode == "Prefix":
        obj.name = value + obj.name
    elif mode == "Set":
        obj.name = value
    elif mode == "Suffix":
        obj.name = obj.name + value
    elif mode == "Replace":
        obj.name = obj.name.replace(value_from, value)
    elif mode == "Blend Name":
        obj.name = Path(bpy.data.filepath).stem


def get_enum_items():
    return (
        ("Set",) * 3,
        ("Prefix",) * 3,
        ("Replace",) * 3,
        ("Suffix",) * 3,
        ("Blend Name",) * 3,
    )


class RenameAssetOperation:
    MAPPING = "RENAME_ASSET"
    LABEL = "Rename Asset"
    DESCRIPTION = "Rename Asset"
    OPERATION = lambda assets, mode, value, value_from: [rename(a, mode, value, value_from, False) for a in assets]
    ATTRIBUTES = ("enum_value", "string_value", "string_value_2")

    @staticmethod
    def get_enum_items():
        return get_enum_items()

    @staticmethod
    def draw(layout, operation_pg):
        layout.prop(operation_pg, "enum_value", text="Mode")
        if operation_pg.enum_value == "Blend Name":
            return
        elif operation_pg.enum_value == "Replace":
            layout.prop(operation_pg, "string_value_2", text="Replace")
            layout.prop(operation_pg, "string_value", text="With")
        else:
            layout.prop(operation_pg, "string_value")


class RenameDataOperation(ObjectFilteredOperation):
    MAPPING = "RENAME_DATA"
    LABEL = "Rename Object's Data"
    DESCRIPTION = "Rename Object's Data"
    OPERATION = lambda assets, mode, value, value_from, same_as_asset: [
        rename(
            a.data,
            "Set" if same_as_asset else mode,
            a.name if same_as_asset else value,
            value_from,
            False,
        )
        for a in assets
        if hasattr(a, "data") and a.data is not None
    ]
    ATTRIBUTES = ("enum_value", "string_value", "string_value_2", "bool_value")

    @staticmethod
    def get_enum_items():
        return get_enum_items()

    @staticmethod
    def draw(layout, operation_pg):
        layout.prop(operation_pg, "bool_value", text="Same as Asset ?")
        if not operation_pg.bool_value:
            layout.prop(operation_pg, "enum_value", text="Mode")
            if operation_pg.enum_value == "Blend Name":
                return
            if operation_pg.enum_value == "Replace":
                layout.prop(operation_pg, "string_value_2", text="Replace")
                layout.prop(operation_pg, "string_value", text="With")
            else:
                layout.prop(operation_pg, "string_value")


class RenameMaterialOperation(ObjectFilteredOperation):
    MAPPING = "RENAME_MATERIAL"
    LABEL = "Rename Object's Material"
    DESCRIPTION = "Rename Object's Material"
    OPERATION = lambda assets, mode, value, value_from, same_as_asset, slot: [
        rename(
            a.data.materials[slot],
            "Replace" if same_as_asset else mode,
            value_from,
            a.name if same_as_asset else value,
            False,
        )
        for a in assets
        if slot >= 0
        and hasattr(a, "data")
        and a.data is not None
        and hasattr(a.data, "materials")
        and len(a.data.materials) > slot
        and a.data.materials[slot] is not None
    ]
    ATTRIBUTES = ("enum_value", "string_value", "string_value_2", "bool_value", "int_value")

    @staticmethod
    def get_enum_items():
        return get_enum_items()

    @staticmethod
    def draw(layout, operation_pg):
        layout.prop(operation_pg, "int_value", text="Slot")
        layout.prop(operation_pg, "bool_value", text="Same as Asset ?")
        if not operation_pg.bool_value:
            layout.prop(operation_pg, "enum_value", text="Mode")
            if operation_pg.enum_value == "Replace":
                layout.prop(operation_pg, "string_value_2", text="Replace")
                layout.prop(operation_pg, "string_value", text="With")
            else:
                layout.prop(operation_pg, "string_value")
