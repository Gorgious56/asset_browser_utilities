import bpy

from asset_browser_utilities.core.test.tool import (
    execute_logic,
    get_asset_filter_settings,
    set_library_export_source,
    setup_and_get_current_operator,
)
from asset_browser_utilities.core.library.prop import LibraryType


class TestOperator:
    def __init__(
        self,
        filepath,
        filter_assets=False,
        filter_types=False,
        filter_object_types=False,
        op_name="",
        logic_class=None,
    ):
        bpy.ops.wm.open_mainfile(filepath=str(filepath))

        set_library_export_source(LibraryType.FileCurrent.value)

        if op_name:
            self.op_props = setup_and_get_current_operator(op_name)

        asset_filter_settings = get_asset_filter_settings()
        asset_filter_settings.filter_assets = filter_assets
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

        self.logic_class = logic_class

    def execute(self):
        execute_logic(self.logic_class)
