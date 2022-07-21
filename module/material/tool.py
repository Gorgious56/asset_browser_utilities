import bpy
import re


def get_all_materials_for_an_enum_selector(self, context):
    mats_enum = get_all_materials_for_an_enum_selector.mats_enum
    mats_enum.clear()
    if hasattr(self, "mode") and self.mode == "Trailing Numbers":
        mats_enum = get_all_materials_without_trailing_numbers()
        return mats_enum
    else:
        mats_enum = [(material.name,) * 3 for material in bpy.data.materials]
        return mats_enum


get_all_materials_for_an_enum_selector.mats_enum = []


def get_all_materials_without_trailing_numbers():
    all_materials = set(m.name for m in bpy.data.materials)
    duplicate_materials = set()
    for material in bpy.data.materials:
        material_name = material.name
        search = re.search("\.[0-9]+$", material_name)
        if search:
            base_name = material_name[0 : search.start()]
            if base_name in all_materials:
                duplicate_materials.add(material_name[0 : search.start()])
    duplicate_materials = sorted(list(duplicate_materials))
    return [(m,) * 3 for m in duplicate_materials]
