from collections import defaultdict
import bpy
from bpy.types import PropertyGroup
from bpy.props import PointerProperty, BoolProperty, EnumProperty, CollectionProperty

from asset_browser_utilities.core.filter.main import AssetFilterSettings
from asset_browser_utilities.core.library.prop import LibraryExportSettings
from asset_browser_utilities.core.operator.prop import CurrentOperatorProperty
from asset_browser_utilities.module.catalog.prop import CatalogExportSettings
from asset_browser_utilities.module.asset.prop import SelectedAssetFiles

from asset_browser_utilities.module.asset.operator.mark import AssetMarkOperatorProperties
from asset_browser_utilities.module.asset.export.operator import AssetExportOperatorProperties
from asset_browser_utilities.module.asset.operator.copy import AssetDataCopyOperatorProperties

from asset_browser_utilities.module.author.set import AuthorSetOperatorProperties

from asset_browser_utilities.module.catalog.operator.sort_like_folders import (
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

from asset_browser_utilities.module.operation.operator.operation import OperationCustomOperatorProperties

from asset_browser_utilities.module.preview.operator.extract import PreviewExtractOperatorProperties
from asset_browser_utilities.module.preview.operator.generate import PreviewGenerateOperatorProperties
from asset_browser_utilities.module.preview.operator.import_ import PreviewImportOperatorProperties

from asset_browser_utilities.module.tag.operator.tool import TagAddOrRemoveOperatorProperties
from asset_browser_utilities.module.tag.operator.add_smart import TagAddSmartOperatorProperties


import sys, inspect


def get_classes():
    return inspect.getmembers(sys.modules[__name__], inspect.isclass)


_TAGS = (
    "Asset",
    "Author",
    "Catalog",
    "CustomProperty",
    "Description",
    "Material",
    "NodeTree",
    "OperationCustom",
    "Preview",
    "Tag",
)
_GROUPS = defaultdict(list)
operator_properties_classes = [cls for cls in get_classes() if cls[0].endswith("OperatorProperties")]

for name, cls in operator_properties_classes:
    for tag in _TAGS:
        if name.startswith(tag):
            _GROUPS[tag].append(cls)
            break


def get_group_sections(self, context):
    if not get_group_sections.items:
        get_group_sections.items = [
            (group_name, Cache.PrettifyClassName(group_name), str([cls.__name__ for cls in classes]))
            for (group_name, classes) in _GROUPS.items()
        ]
    return get_group_sections.items


get_group_sections.items = []


class Cache(PropertyGroup):
    # Settings
    library_settings: PointerProperty(type=LibraryExportSettings)
    asset_filter_settings: PointerProperty(type=AssetFilterSettings)
    catalog_settings: PointerProperty(type=CatalogExportSettings)

    # Operator properties
    op_current: PointerProperty(type=CurrentOperatorProperty)

    selected_assets: PointerProperty(type=SelectedAssetFiles)

    # UI settings

    show: BoolProperty()
    group_section: EnumProperty(items=get_group_sections)

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

    @staticmethod
    def init():
        # We initialize all the class properties as dynamic attributes of the class.
        # We use the __annotations__ for that
        # See https://blender.stackexchange.com/a/161533/86891
        def class_name_to_attribute_name(name: str):
            name = name.replace("OperatorProperties", "")
            name = "op" + "".join("_" + char.lower() if char.isupper() else char.strip() for char in name).strip()
            return name

        bpy.utils.unregister_class(Cache)

        Cache.__annotations__.update(
            {
                class_name_to_attribute_name(name): PointerProperty(type=cls)
                for name, cls in operator_properties_classes
            }
        )

        bpy.utils.register_class(Cache)
