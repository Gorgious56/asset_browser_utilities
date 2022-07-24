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
        materials_to = [op_props.material_to]
        material_from = bpy.data.materials.get(op_props.material_from)

        for material_to in materials_to:
            for asset in self.assets:
                if not hasattr(asset, "material_slots"):
                    continue
                for m_s in asset.material_slots:
                    if m_s.material is None:
                        continue
                    if m_s.material.name in materials_to:
                        material_to = m_s.material
                        m_s.material = material_from
                        Logger.display(f"{repr(material_to)} replaced by '{repr(material_from)}' in {repr(asset)}")

        self.save_file()
        self.execute_next_blend()


class MaterialReplaceOperatorProperties(PropertyGroup):
    material_to: EnumProperty(name="Replace", items=get_all_materials_for_an_enum_selector)
    material_from: EnumProperty(name="With", items=get_all_materials_for_an_enum_selector)

    def draw(self, layout):
        box = layout.box()
        box.prop(self, "material_to")
        box.prop(self, "material_from")


class ABU_OT_material_replace(Operator, BatchFolderOperator):
    bl_idname = "abu.material_replace"
    bl_label = "Replace Materials"
    bl_description = "Replace a material with another one"

    operator_settings: PointerProperty(type=MaterialReplaceOperatorProperties)
    logic_class = MaterialReplaceBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets_optional=True, filter_assets=True)
