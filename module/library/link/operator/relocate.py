import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.operator.tool import (
    BatchFolderOperator,
    BaseOperatorProps,
)

from asset_browser_utilities.module.library.link.prop import AssetLibraryDummy
from asset_browser_utilities.module.library.link.tool import link_from_asset_dummy


class AssetLinkRelocateOperatorProperties(PropertyGroup, BaseOperatorProps):
    library: PointerProperty(type=AssetLibraryDummy)

    def draw(self, layout, context=None):
        return

    def init(self, from_current_file=False):
        self.library.populate()

    def run_in_file(self, attributes=None):
        should_save = False
        for blend_data_library in bpy.data.libraries:
            if blend_data_library.is_missing:
                for asset_dummy in blend_data_library.abu_asset_library_dummy.assets:
                    corresponding_asset_dummy = next((self.library.by_uuid(asset_dummy.uuid)), None)
                    if corresponding_asset_dummy:
                        should_save = True
                        link_from_asset_dummy(
                            corresponding_asset_dummy,
                            asset_dummy.asset.get(),
                            purge=True,
                        )
            for linked_asset in blend_data_library.users_id:
                if linked_asset.is_missing:
                    for linked_asset_dummy in blend_data_library.abu_asset_library_dummy.assets:
                        if linked_asset_dummy.asset.get() == linked_asset:
                            corresponding_asset_dummy = next((self.library.by_uuid(linked_asset_dummy.uuid)), None)
                            if corresponding_asset_dummy:
                                should_save = True
                                link_from_asset_dummy(corresponding_asset_dummy, linked_asset, purge=True)
                                break
        return should_save


class ABU_OT_asset_link_relocate(Operator, BatchFolderOperator):
    ui_library = LibraryType.UserLibrary.value
    bl_idname = "abu.asset_link_relocate"
    bl_label = "Batch Relocate Links"
    bl_description = "Batch relocate linked assets from an asset library"

    operator_settings: PointerProperty(type=AssetLinkRelocateOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
