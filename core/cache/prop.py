from bpy.types import PropertyGroup
from bpy.props import PointerProperty, BoolProperty, EnumProperty, CollectionProperty

from asset_browser_utilities.core.filter.main import AssetFilterSettings
from asset_browser_utilities.core.library.prop import LibraryExportSettings
from asset_browser_utilities.core.operator.prop import CurrentOperatorProperty
from asset_browser_utilities.module.catalog.prop import CatalogExportSettings
from asset_browser_utilities.module.asset.prop import SelectedAssetFiles

from asset_browser_utilities.module.asset.operator.mark import AssetMarkOperatorProperties
from asset_browser_utilities.module.asset.export.operator import AssetExportOperatorProperties
from asset_browser_utilities.module.asset.operator.copy import AssetCopyDataOperatorProperties

from asset_browser_utilities.module.author.set import AuthorSetOperatorProperties

from asset_browser_utilities.module.catalog.operator.sort_catalogs_like_folders import (
    CatalogSortLikeFoldersOperatorProperties,
)
from asset_browser_utilities.module.catalog.operator.move_from_a_to_b import CatalogMoveFromAToBOperatorProperties
from asset_browser_utilities.module.catalog.operator.move_to import CatalogMoveOperatorProperties
from asset_browser_utilities.module.catalog.operator.remove_from import CatalogRemoveFromOperatorProperties
from asset_browser_utilities.module.catalog.operator.remove_empty import CatalogRemoveEmptyOperatorProperties

from asset_browser_utilities.module.custom_property.operator.set import CustomPropertySetOperatorProperties
from asset_browser_utilities.module.custom_property.operator.remove import CustomPropertyRemoveOperatorProperties

from asset_browser_utilities.module.description.set import DescriptionSetOperatorProperties

from asset_browser_utilities.module.material.operator.merge import MaterialMergeOperatorProperties
from asset_browser_utilities.module.material.operator.replace import MaterialReplaceOperatorProperties

from asset_browser_utilities.module.node_tree.operator.merge import NodeTreeMergeOperatorProperties
from asset_browser_utilities.module.node_tree.operator.replace import NodeTreeReplaceOperatorProperties

from asset_browser_utilities.module.operation.operator.operation import OperationOperatorProperties

from asset_browser_utilities.module.preview.operator.extract import PreviewExtractOperatorProperties
from asset_browser_utilities.module.preview.operator.generate import PreviewGenerateOperatorProperties
from asset_browser_utilities.module.preview.operator.import_ import PreviewImportOperatorProperties

from asset_browser_utilities.module.tag.operator.tool import TagAddOrRemoveOperatorProperties
from asset_browser_utilities.module.tag.operator.add_smart import TagAddSmartOperatorProperties


_GROUPS = {
    "Asset": (
        AssetCopyDataOperatorProperties,
        AssetExportOperatorProperties,
        AssetMarkOperatorProperties,
    ),
    "Author": (AuthorSetOperatorProperties,),
    "Catalog": (
        CatalogMoveFromAToBOperatorProperties,
        CatalogMoveOperatorProperties,
        CatalogRemoveFromOperatorProperties,
        CatalogRemoveEmptyOperatorProperties,
        CatalogSortLikeFoldersOperatorProperties,
    ),
    "Custom Property": (CustomPropertySetOperatorProperties, CustomPropertyRemoveOperatorProperties),
    "Description": (DescriptionSetOperatorProperties,),
    "Material": (MaterialMergeOperatorProperties, MaterialReplaceOperatorProperties),
    "Node Tree": (NodeTreeMergeOperatorProperties, NodeTreeReplaceOperatorProperties),
    "Custom Operation": (OperationOperatorProperties,),
    "Preview": (PreviewGenerateOperatorProperties, PreviewExtractOperatorProperties, PreviewImportOperatorProperties),
    "Tag": (TagAddSmartOperatorProperties, TagAddOrRemoveOperatorProperties),
}


class ShowOpProperty(PropertyGroup):
    show: BoolProperty()


class Cache(PropertyGroup):
    # Settings
    library_settings: PointerProperty(type=LibraryExportSettings)
    asset_filter_settings: PointerProperty(type=AssetFilterSettings)
    catalog_settings: PointerProperty(type=CatalogExportSettings)

    # Operator properties
    op_current: PointerProperty(type=CurrentOperatorProperty)

    op_copy_data: PointerProperty(type=AssetCopyDataOperatorProperties)
    op_export: PointerProperty(type=AssetExportOperatorProperties)
    op_mark: PointerProperty(type=AssetMarkOperatorProperties)

    op_author_set: PointerProperty(type=AuthorSetOperatorProperties)

    op_catalog_move_from_a_to_b: PointerProperty(type=CatalogMoveFromAToBOperatorProperties)
    op_catalog_move: PointerProperty(type=CatalogMoveOperatorProperties)
    op_catalog_remove: PointerProperty(type=CatalogRemoveFromOperatorProperties)
    op_catalog_remove_empty: PointerProperty(type=CatalogRemoveEmptyOperatorProperties)
    op_catalog_sort_like_folders: PointerProperty(type=CatalogSortLikeFoldersOperatorProperties)

    op_custom_prop_set: PointerProperty(type=CustomPropertySetOperatorProperties)
    op_custom_prop_remove: PointerProperty(type=CustomPropertyRemoveOperatorProperties)

    op_description_set: PointerProperty(type=DescriptionSetOperatorProperties)

    op_material_merge: PointerProperty(type=MaterialMergeOperatorProperties)
    op_material_replace: PointerProperty(type=MaterialReplaceOperatorProperties)

    op_node_tree_merge: PointerProperty(type=NodeTreeMergeOperatorProperties)
    op_node_tree_replace: PointerProperty(type=NodeTreeReplaceOperatorProperties)

    op_operation_custom: PointerProperty(type=OperationOperatorProperties)

    op_preview_generate: PointerProperty(type=PreviewGenerateOperatorProperties)
    op_preview_extract: PointerProperty(type=PreviewExtractOperatorProperties)
    op_preview_import: PointerProperty(type=PreviewImportOperatorProperties)

    op_tag_smart_add: PointerProperty(type=TagAddSmartOperatorProperties)
    op_tag_add_or_remove: PointerProperty(type=TagAddOrRemoveOperatorProperties)

    selected_assets: PointerProperty(type=SelectedAssetFiles)

    # UI settings

    show: BoolProperty()
    group_section: EnumProperty(
        items=lambda self, context: [
            (group_name, group_name, str([cls.__name__ for cls in classes]))
            for (group_name, classes) in _GROUPS.items()
        ]
    )
    show_op: CollectionProperty(type=ShowOpProperty)

    def get(self, _type):
        if isinstance(_type, str):
            return getattr(self, _type)
        for prop_name in self.__annotations__:
            prop = getattr(self, prop_name)
            if isinstance(prop, _type):
                return prop

    def get_prop_name(self, _type):
        if isinstance(_type, str):
            return getattr(self, _type)
        for prop_name in self.__annotations__:
            prop = getattr(self, prop_name)
            if isinstance(prop, _type):
                return prop_name

    @staticmethod
    def PrettifyClassName(name):
        # https://stackoverflow.com/a/45778633/7092409
        return "".join(" " + char if char.isupper() else char.strip() for char in name).strip()

    def draw(self, layout, context, header=None, rename=False):
        if header is None:
            header = self.name
        row = layout.row(align=True)
        if rename:
            row.prop(self, "name")
        row.prop(self, "show", toggle=True, text=header)
        if not self.show:
            return
        grid = layout.grid_flow(row_major=True, align=True)
        for group in _GROUPS.keys():
            grid.prop_enum(self, "group_section", group)
        for cls in _GROUPS.get(self.group_section):
            attr = self.get_prop_name(cls)
            default_setting = getattr(self, attr)
            if hasattr(default_setting, "draw"):
                box = layout.box()
                box.label(text=Cache.PrettifyClassName(default_setting.__class__.__name__), icon="TOOL_SETTINGS")
                default_setting.draw(box, context)
