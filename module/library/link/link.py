import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty

from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.filter.container import get_all_assets_in_file
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.library.tool import get_directory_name
from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator

from asset_browser_utilities.module.library.link.prop import AssetLibrary
from asset_browser_utilities.module.library.link.tool import link_from_asset_dummy


class AssetLinkBatchExecute(BatchExecute):
    def __init__(self, file_extension="blend"):
        get_current_operator_properties().library.populate()
        super().__init__(file_extension)

    def execute_one_file_and_the_next_when_finished(self):
        library_dummy = get_current_operator_properties().library
        asset_dummies = library_dummy.by_filepath(bpy.data.filepath)
        assets_to_keep = []
        for asset_dummy in asset_dummies:
            assets_to_keep.append(getattr(bpy.data, asset_dummy.blenddata_name)[asset_dummy.name])
        all_assets_in_file = list(get_all_assets_in_file())
        assets_to_discard = set(all_assets_in_file) - set(assets_to_keep)
        for asset_to_discard in assets_to_discard:
            corresponding_asset_dummy = next(
                (library_dummy.by_directory_and_name(get_directory_name(asset_to_discard), asset_to_discard.name)),
                None,
            )
            if corresponding_asset_dummy:
                link_from_asset_dummy(corresponding_asset_dummy, asset_to_discard)
        self.save_file()
        self.execute_next_file()


class AssetLinkOperatorProperties(PropertyGroup):
    library: PointerProperty(type=AssetLibrary)

    def draw(self, layout, context=None):
        return


class ABU_OT_asset_link(Operator, BatchFolderOperator):
    ui_library = LibraryType.UserLibrary.value
    bl_idname = "abu.asset_link"
    bl_label = "Batch Link Assets"
    bl_description = "Batch link assets from an asset library"

    operator_settings: PointerProperty(type=AssetLinkOperatorProperties)
    logic_class = AssetLinkBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
