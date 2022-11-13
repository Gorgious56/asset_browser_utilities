from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, EnumProperty
from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.filter.main import AssetFilterSettings

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator


class BlendRenameBatchExecute(BatchExecute):
    def execute_next_blend(self):
        op_prop = get_current_operator_properties()
        filter_name = get_from_cache(AssetFilterSettings).filter_name
        for blend in self.blends:
            if filter_name.filter(blend.stem):
                old_name = str(blend)
                folder_name = blend.parent.name
                new_name = blend.with_stem(folder_name)
                while new_name.exists():
                    new_name = new_name.with_stem(str(new_name.stem) + "_")
                blend.rename(new_name)
                Logger.display(f"Renamed {old_name} to {new_name}")


class BlendRenameOperatorProperties(PropertyGroup):
    mode: EnumProperty(items=(("Folder Name",) * 3,))

    def draw(self, layout, context=None):
        layout.prop(self, "mode")


class ABU_OT_blend_rename(Operator, BatchFolderOperator):
    bl_idname = "abu.blend_rename"
    bl_label = "Rename Blend File"

    operator_settings: PointerProperty(type=BlendRenameOperatorProperties)
    logic_class = BlendRenameBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=False, filter_type=False, filter_selection=False)
