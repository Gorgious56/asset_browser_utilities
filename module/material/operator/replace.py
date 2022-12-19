import bpy

from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, EnumProperty

from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator

from asset_browser_utilities.module.material.tool import get_all_materials_for_an_enum_selector


class MaterialReplaceBatchExecute(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        op_props = get_current_operator_properties()
        material_to_override = bpy.data.materials.get(op_props.material_to_override)
        material_to_keep = bpy.data.materials.get(op_props.material_to_keep)
        material_to_override.user_remap(material_to_keep)
        Logger.display(f"Replaced {repr(material_to_override)} with {repr(material_to_keep)}")

        self.save_file()
        self.execute_next_file()


class MaterialReplaceOperatorProperties(PropertyGroup):
    material_to_override: EnumProperty(name="Replace", items=get_all_materials_for_an_enum_selector)
    material_to_keep: EnumProperty(name="With", items=get_all_materials_for_an_enum_selector)

    def draw(self, layout, context=None):
        box = layout.box()
        box.prop(self, "material_to_override")
        box.prop(self, "material_to_keep")


class ABU_OT_material_replace(Operator, BatchFolderOperator):
    bl_idname = "abu.material_replace"
    bl_label = "Replace Materials"
    bl_description = "Replace a material with another one"

    operator_settings: PointerProperty(type=MaterialReplaceOperatorProperties)
    logic_class = MaterialReplaceBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
