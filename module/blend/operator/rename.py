from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, EnumProperty

from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.filter.main import AssetFilterSettings
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps


class BlendRenameOperatorProperties(PropertyGroup, BaseOperatorProps):
    mode: EnumProperty(items=(("Folder Name",) * 3,))

    def draw(self, layout, context=None):
        layout.prop(self, "mode")

    def run_in_file(self, attributes=None):
        filter_name = get_from_cache(AssetFilterSettings).filter_name
        for blend in self.files:
            if filter_name.filter(blend.stem):
                if self.mode == "Folder Name":
                    old_name = str(blend)
                    folder_name = blend.parent.name
                    new_name = blend.with_stem(folder_name)
                    blend.rename(new_name)
                    Logger.display(f"Renamed {old_name} to {new_name}")


class ABU_OT_blend_rename(Operator, BatchFolderOperator):
    bl_idname = "abu.blend_rename"
    bl_label = "Rename Blend File"

    operator_settings: PointerProperty(type=BlendRenameOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=False, filter_type=False, filter_selection=False)
