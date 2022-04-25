from bpy.types import Panel, AssetMetaData
from rna_prop_ui import PropertyPanel


class ABU_PT_asset_meta_data_custom_properties(Panel, PropertyPanel):
    _context_path = "id.asset_data"
    _property_type = AssetMetaData
    bl_label = "Custom Properties"
    bl_idname = "ABU_PT_asset_meta_data_custom_properties"
    bl_space_type = "FILE_BROWSER"
    bl_region_type = "TOOL_PROPS"
