import sys
from inspect import getmembers, isclass

import bpy
from bpy.types import PropertyGroup
from bpy.props import PointerProperty, BoolProperty, EnumProperty

from asset_browser_utilities.core.filter.main import AssetFilterSettings
from asset_browser_utilities.core.library.prop import LibraryExportSettings
from asset_browser_utilities.core.operator.prop import CurrentOperatorProperty
from asset_browser_utilities.module.catalog.prop import CatalogExportSettings
from asset_browser_utilities.module.asset.prop import SelectedAssetFiles


def get_group_sections(self, context):
    if not get_group_sections.items:
        get_group_sections.items = [
            (group_name, Cache.PrettifyClassName(group_name), str([cls.__name__ for cls in classes]))
            for (group_name, classes) in Cache._GROUPS.items()
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

    _GROUPS = {}
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
        return (
            "".join(" " + char if char.isupper() else char.strip() for char in name)
            .strip()
            .replace("Operator Properties", "")
        )

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
        for group in Cache._GROUPS.keys():
            grid.prop_enum(self, "group_section", group)
        for cls in Cache._GROUPS.get(self.group_section):
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
        for module_name, module in sys.modules.items():
            if not module_name.startswith("asset_browser_utilities.module"):
                continue
            module_name_split = module_name.split(".")
            if len(module_name_split) > 2:
                tag = module_name_split[2].title().replace("_", " ")
                if tag not in Cache._GROUPS.keys():
                    Cache._GROUPS[tag] = []
            for class_name, cls in getmembers(module, isclass):
                if class_name.endswith("OperatorProperties"):
                    Cache.__annotations__[class_name_to_attribute_name(class_name)] = PointerProperty(type=cls)
                    Cache._GROUPS[tag].append(cls)
                    break
        empty_tags = []
        for tag, classes in Cache._GROUPS.items():
            if not classes:
                empty_tags.append(tag)
        for tag in empty_tags:
            del Cache._GROUPS[tag]
        bpy.utils.register_class(Cache)
