import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, EnumProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps

from asset_browser_utilities.module.material.tool import get_all_materials_for_an_enum_selector


class MaterialReplaceOperatorProperties(PropertyGroup, BaseOperatorProps):
    material_to_override: EnumProperty(name="Replace", items=get_all_materials_for_an_enum_selector)
    material_to_keep: EnumProperty(name="With", items=get_all_materials_for_an_enum_selector)

    def draw(self, layout, context=None):
        box = layout.box()
        box.prop(self, "material_to_override")
        box.prop(self, "material_to_keep")

    def runin_file(self):
        material_to_override = bpy.data.materials.get(self.material_to_override)
        material_to_keep = bpy.data.materials.get(self.material_to_keep)
        material_to_override.user_remap(material_to_keep)
        Logger.display(f"Replaced {repr(material_to_override)} with {repr(material_to_keep)}")


class ABU_OT_material_replace(Operator, BatchFolderOperator):
    bl_idname = "abu.material_replace"
    bl_label = "Replace Materials"
    bl_description = "Replace a material with another one"

    operator_settings: PointerProperty(type=MaterialReplaceOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
