import bpy
import re

from asset_browser_utilities.module.material.tool import get_all_materials_for_an_enum_selector
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, EnumProperty, BoolProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps


class MaterialMergeOperatorProperties(PropertyGroup, BaseOperatorProps):
    mode: EnumProperty(
        name="Mode", items=(("Trailing Numbers", "Trailing Numbers", "Trailing Numbers", "LINENUMBERS_ON", 0),)
    )
    execute_all: BoolProperty(name="Merge all duplicate materials", default=False)
    material_name: EnumProperty(name="Base Material", items=get_all_materials_for_an_enum_selector)

    def draw(self, layout, context=None):
        box = layout.box()
        box.label(text="Merge materials")
        box.prop(self, "mode")
        box.prop(self, "execute_all")
        if not self.execute_all:
            box.prop(self, "material_name")

    def run_in_file(self, attributes=None):
        if self.execute_all:
            materials_to = [
                bpy.data.materials.get(mat_name[0]) for mat_name in get_all_materials_for_an_enum_selector(self, None)
            ]
        else:
            materials_to = [bpy.data.materials.get(self.material_name)]
        materials_to_names = [m.name for m in materials_to]

        if self.mode == "Trailing Numbers":
            for material_to in materials_to:
                materials_from = set()
                for material in bpy.data.materials:
                    material_name = material.name
                    if material_name in materials_to_names:
                        continue
                    search = re.search("\.[0-9]+$", material_name)
                    if search and material_name[0 : search.start()] == material_to.name:
                        materials_from.add(material)
                for material in materials_from:
                    material.user_remap(material_to)
                    Logger.display(f"Replaced {repr(material)} by {repr(material_to)}")


class ABU_OT_material_merge(Operator, BatchFolderOperator):
    bl_idname = "abu.material_merge"
    bl_label = "Merge Materials"
    bl_description = "Merge materials finishing with .001, .002 etc with base material"

    operator_settings: PointerProperty(type=MaterialMergeOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
