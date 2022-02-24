import bpy.app
from bpy.types import PropertyGroup
from bpy.props import BoolProperty, EnumProperty

from asset_browser_utilities.core.helper import copy_simple_property_group

_flag_types = list(range(40))
_flag_types_object = list(range(20))


def get_types():
    if bpy.app.version > (3, 1, 0):
        return (
            ("actions", "Actions", "Actions", "ACTION", 2 ** _flag_types.pop(0)),
            ("brushes", "Brushes", "Brushes", "BRUSH_DATA", 2 ** _flag_types.pop(0)),
            ("cache_files", "Cache Files", "Cache Files", "FILE_CACHE", 2 ** _flag_types.pop(0)),
            ("collections", "Collections", "Collections", "OUTLINER_COLLECTION", 2 ** _flag_types.pop(0)),
            ("images", "Images", "Images", "IMAGE_DATA", 2 ** _flag_types.pop(0)),
            ("materials", "Materials", "Materials", "MATERIAL", 2 ** _flag_types.pop(0)),
            ("node_groups", "Node Trees", "Node Trees", "NODETREE", 2 ** _flag_types.pop(0)),
            ("objects", "Objects", "Objects", "OBJECT_DATA", 2 ** _flag_types.pop(0)),
            ("palettes", "Palettes", "Palettes", "COLOR", 2 ** _flag_types.pop(0)),
            ("scenes", "Scenes", "Scenes", "SCENE_DATA", 2 ** _flag_types.pop(0)),
            ("texts", "Texts", "Texts", "TEXT", 2 ** _flag_types.pop(0)),
            ("textures", "Textures", "Textures", "TEXTURE_DATA", 2 ** _flag_types.pop(0)),
            ("worlds", "Worlds", "Worlds", "WORLD", 2 ** _flag_types.pop(0)),
            ("workspaces", "Workspaces", "Workspaces", "WORKSPACE", 2 ** _flag_types.pop(0)),
        )
    elif bpy.app.version > (3, 0, 0):
        return (
            ("actions", "Actions", "Action", "ACTION", 2 ** _flag_types.pop(0)),
            ("materials", "Materials", "Materials", "MATERIAL", 2 ** _flag_types.pop(0)),
            ("node_groups", "Node Trees", "Node Trees", "NODETREE", 2 ** _flag_types.pop(0)),
            ("objects", "Objects", "Objects", "OBJECT_DATA", 2 ** _flag_types.pop(0)),
            ("worlds", "Worlds", "Worlds", "WORLD", 2 ** _flag_types.pop(0)),
        )
    return (
        ("actions", "Actions", "Action", "ACTION", 2 ** _flag_types.pop(0)),
        ("materials", "Materials", "Materials", "MATERIAL", 2 ** _flag_types.pop(0)),
        ("objects", "Objects", "Objects", "OBJECT_DATA", 2 ** _flag_types.pop(0)),
        ("worlds", "Worlds", "Worlds", "WORLD", 2 ** _flag_types.pop(0)),
    )


class FilterTypes(PropertyGroup):
    types: EnumProperty(
        options={"ENUM_FLAG"},
        items=get_types(),
        default={"objects"},
    )
    types_object_filter: BoolProperty(default=False, name="Filter Objects")
    types_object: EnumProperty(
        options={"ENUM_FLAG"},
        items=(
            ("ARMATURE", "Armature", "Armature", "ARMATURE_DATA", 2 ** _flag_types_object.pop(0)),
            ("CAMERA", "Camera", "Camera", "CAMERA_DATA", 2 ** _flag_types_object.pop(0)),
            ("CURVE", "Curve", "Curve", "CURVE_DATA", 2 ** _flag_types_object.pop(0)),
            ("EMPTY", "Empty", "Empty", "EMPTY_DATA", 2 ** _flag_types_object.pop(0)),
            (
                "GREASEPENCIL",
                "Grease Pencil",
                "Grease Pencil",
                "OUTLINER_DATA_GREASEPENCIL",
                2 ** _flag_types_object.pop(0),
            ),
            ("HAIR", "Hair", "Hair", "HAIR_DATA", 2 ** _flag_types_object.pop(0)),
            ("LIGHT", "Light", "Light", "LIGHT", 2 ** _flag_types_object.pop(0)),
            (
                "LIGHT_PROBE",
                "Light Probe",
                "Light Probe",
                "OUTLINER_DATA_LIGHTPROBE",
                2 ** _flag_types_object.pop(0),
            ),
            ("LATTICE", "Lattice", "Lattice", "LATTICE_DATA", 2 ** _flag_types_object.pop(0)),
            ("MESH", "Mesh", "Mesh", "MESH_DATA", 2 ** _flag_types_object.pop(0)),
            ("META", "Metaball", "Metaball", "META_DATA", 2 ** _flag_types_object.pop(0)),
            ("POINTCLOUD", "Point Cloud", "Point Cloud", "POINTCLOUD_DATA", 2 ** _flag_types_object.pop(0)),
            ("SPEAKER", "Speaker", "Speaker", "OUTLINER_DATA_SPEAKER", 2 ** _flag_types_object.pop(0)),
            ("SURFACE", "Surface", "Surface", "SURFACE_DATA", 2 ** _flag_types_object.pop(0)),
            ("VOLUME", "Volume", "Volume", "VOLUME_DATA", 2 ** _flag_types_object.pop(0)),
            ("FONT", "Text", "Text", "FONT_DATA", 2 ** _flag_types_object.pop(0)),
        ),
        default={
            "CURVE",
            "MESH",
        },
    )

    def draw(self, layout):
        box = layout.box()
        box.label(text="Filter By Type", icon="FILTER")
        col = box.column(align=True)
        for filter_type in self.bl_rna.properties["types"].enum_items_static:
            row = col.row(align=True)
            row.prop_enum(self, "types", filter_type.identifier)
            if filter_type.identifier == "objects":
                self.draw_object_types_selector(col, row)

    def draw_object_types_selector(self, layout_items, layout_filter):
        layout_filter.prop(self, "types_object_filter", text="", icon="FILTER")
        if self.types_object_filter and "objects" in self.types:
            box_object = layout_items.box()
            col_object = box_object.column(align=True)
            for filter_type_obj in self.bl_rna.properties["types_object"].enum_items_static:
                col_object.prop_enum(self, "types_object", filter_type_obj.identifier)
