from asset_browser_utilities.module.node_tree.operator.merge import NodeTreeMergeOperatorProperties
from bpy.types import PropertyGroup
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.core.filter.main import AssetFilterSettings
from asset_browser_utilities.core.library.prop import LibraryExportSettings
from asset_browser_utilities.core.operator.operation import OperationSettings
from asset_browser_utilities.core.operator.prop import CurrentOperatorProperty
from asset_browser_utilities.module.catalog.prop import CatalogExportSettings
from asset_browser_utilities.module.asset.prop import SelectedAssetFiles

from asset_browser_utilities.module.asset.operator.mark import AssetMarkOperatorProperties
from asset_browser_utilities.module.asset.export.operator import AssetExportOperatorProperties
from asset_browser_utilities.module.author.set import AuthorSetOperatorProperties
from asset_browser_utilities.module.asset.operator.copy import AssetCopyDataOperatorProperties
from asset_browser_utilities.module.catalog.operator.sort_catalogs_like_folders import (
    CatalogSortLikeFoldersOperatorProperties,
)
from asset_browser_utilities.module.catalog.operator.move_from_a_to_b import CatalogMoveFromAToBOperatorProperties
from asset_browser_utilities.module.catalog.operator.move_to import CatalogMoveOperatorProperties
from asset_browser_utilities.module.catalog.operator.remove_from import CatalogRemoveFromOperatorProperties
from asset_browser_utilities.module.custom_property.operator.set import CustomPropertySetOperatorProperties
from asset_browser_utilities.module.custom_property.operator.remove import RemoveCustomPropertyOperatorProperties
from asset_browser_utilities.module.description.set import DescriptionSetOperatorProperties
from asset_browser_utilities.module.tag.operator.tool import TagAddOrRemoveOperatorProperties
from asset_browser_utilities.module.tag.operator.add_smart import TagAddSmartOperatorProperties
from asset_browser_utilities.module.material.operator.merge import MaterialMergeOperatorProperties
from asset_browser_utilities.module.preview.operator.extract import PreviewExtractOperatorProperties
from asset_browser_utilities.module.preview.operator.generate import PreviewGenerateOperatorProperties


class Cache(PropertyGroup):
    # Settings
    library_settings: PointerProperty(type=LibraryExportSettings)
    operation_settings: PointerProperty(type=OperationSettings)
    asset_filter_settings: PointerProperty(type=AssetFilterSettings)
    catalog_settings: PointerProperty(type=CatalogExportSettings)

    # Operator properties
    op_current: PointerProperty(type=CurrentOperatorProperty)
    op_mark: PointerProperty(type=AssetMarkOperatorProperties)
    op_copy_data: PointerProperty(type=AssetCopyDataOperatorProperties)
    op_export: PointerProperty(type=AssetExportOperatorProperties)
    op_tag_smart_add: PointerProperty(type=TagAddSmartOperatorProperties)
    op_tag_add_or_remove: PointerProperty(type=TagAddOrRemoveOperatorProperties)
    op_custom_prop_set: PointerProperty(type=CustomPropertySetOperatorProperties)
    op_custom_prop_remove: PointerProperty(type=RemoveCustomPropertyOperatorProperties)
    op_preview_generate: PointerProperty(type=PreviewGenerateOperatorProperties)
    op_preview_extract: PointerProperty(type=PreviewExtractOperatorProperties)
    op_catalog_move_from_a_to_b: PointerProperty(type=CatalogMoveFromAToBOperatorProperties)
    op_catalog_move: PointerProperty(type=CatalogMoveOperatorProperties)
    op_catalog_remove: PointerProperty(type=CatalogRemoveFromOperatorProperties)
    op_catalog_sort_like_folders: PointerProperty(type=CatalogSortLikeFoldersOperatorProperties)
    op_author_set: PointerProperty(type=AuthorSetOperatorProperties)
    op_description_set: PointerProperty(type=DescriptionSetOperatorProperties)
    op_material_merge: PointerProperty(type=MaterialMergeOperatorProperties)
    op_node_tree_merge: PointerProperty(type=NodeTreeMergeOperatorProperties)

    selected_assets: PointerProperty(type=SelectedAssetFiles)

    show: BoolProperty()

    def get(self, _type):
        for prop_name in self.__annotations__:
            prop = getattr(self, prop_name)
            if isinstance(prop, _type):
                return prop

    def draw(self, layout, context, header=None, rename=False):
        if header is None:
            header = self.name
        row = layout.row(align=True)
        if rename:
            row.prop(self, "name")
        row.prop(self, "show", toggle=True, text=header)
        if self.show:
            for attr in self.__annotations__:
                default_setting = getattr(self, attr)
                if hasattr(default_setting, "draw"):
                    default_setting.draw(layout, context)
