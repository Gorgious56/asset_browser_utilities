from asset_browser_utilities.core.cache.prop import Cache
import bpy

from asset_browser_utilities.core.test.tool import (
    execute_logic,
    get_asset_filter_settings,
    set_library_export_source,
    setup_and_get_current_operator,
)
from asset_browser_utilities.core.library.prop import LibraryType


def class_name_to_op_name(name: str):
    name = name.replace("BatchExecute", "")
    name = "op" + "".join("_" + char.lower() if char.isupper() else char.strip() for char in name).strip()
    return name


class TestOperator:
    def __init__(
        self,
        filepath,
        filter_assets=False,
        filter_types=False,
        filter_object_types=False,
        filter_selection=False,
        filter_name=False,
        filter_catalog=False,
        logic_class=None,
    ):
        bpy.ops.wm.open_mainfile(filepath=str(filepath))

        set_library_export_source(LibraryType.FileCurrent.value)

        if logic_class:
            self.op_props = setup_and_get_current_operator(class_name_to_op_name(logic_class.__name__))

        asset_filter_settings = get_asset_filter_settings()
        asset_filter_settings.filter_assets.active = filter_assets
        asset_filter_settings.filter_assets.only_assets = filter_assets

        if bool(filter_types):
            asset_filter_settings.filter_types.types_global_filter = True
            asset_filter_settings.filter_types.types = filter_types
        else:
            asset_filter_settings.filter_types.types_global_filter = False

        if bool(filter_object_types):
            asset_filter_settings.filter_types.types_object_filter = True
            asset_filter_settings.filter_types.types_object = filter_object_types
        else:
            asset_filter_settings.filter_types.types_object_filter = False

        if bool(filter_selection):
            asset_filter_settings.filter_selection.active = True
        else:
            asset_filter_settings.filter_selection.active = False

        if bool(filter_name):
            asset_filter_settings.filter_name.active = True
        else:
            asset_filter_settings.filter_name.active = False

        if bool(filter_catalog):
            asset_filter_settings.filter_catalog.active = True
        else:
            asset_filter_settings.filter_catalog.active = False

        self.logic_class = logic_class

    def execute(self):
        execute_logic(self.logic_class)
