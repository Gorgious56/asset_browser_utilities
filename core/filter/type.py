import bpy.app
from bpy.types import PropertyGroup
from bpy.props import BoolProperty, EnumProperty


flags_enum = iter(range(1, 100, 1))
asset_types = [
    ("actions", "Actions", "Action", "ACTION", 2 ** next(flags_enum)),
    ("materials", "Materials", "Materials", "MATERIAL", 2 ** next(flags_enum)),
    ("objects", "Objects", "Objects", "OBJECT_DATA", 2 ** next(flags_enum)),
    ("worlds", "Worlds", "Worlds", "WORLD", 2 ** next(flags_enum)),
]
if bpy.app.version >= (3, 1, 0):
    asset_types.append(("node_groups", "Node Trees", "Node Trees", "NODETREE", 2 ** next(flags_enum)))
if bpy.app.version >= (3, 2, 0):
    asset_types.append(("collections", "Collections", "Collections", "OUTLINER_COLLECTION", 2 ** next(flags_enum)))
if bpy.app.version >= (3, 3, 0):
    asset_types.extend(
        (
            ("hair_curves", "Hairs", "Hairs", "CURVES_DATA", 2 ** next(flags_enum)),
            ("brushes", "Brushes", "Brushes", "BRUSH_DATA", 2 ** next(flags_enum)),
            ("cache_files", "Cache Files", "Cache Files", "FILE_CACHE", 2 ** next(flags_enum)),
            ("linestyles", "Freestyle Linestyles", "", "LINE_DATA", 2 ** next(flags_enum)),
            ("images", "Images", "Images", "IMAGE_DATA", 2 ** next(flags_enum)),
            ("meshes", "Meshes", "Meshes", "MESH_DATA", 2 ** next(flags_enum)),
            ("masks", "Masks", "Masks", "MOD_MASK", 2 ** next(flags_enum)),
            ("movieclips", "Movie Clips", "Movie Clips", "FILE_MOVIE", 2 ** next(flags_enum)),
            ("paint_curves", "Paint Curves", "Paint Curves", "CURVE_BEZCURVE", 2 ** next(flags_enum)),
            ("palettes", "Palettes", "Palettes", "COLOR", 2 ** next(flags_enum)),
            ("particles", "Particle Systems", "Particle Systems", "PARTICLES", 2 ** next(flags_enum)),
            ("scenes", "Scenes", "Scenes", "SCENE_DATA", 2 ** next(flags_enum)),
            ("sounds", "Sounds", "Sounds", "SOUND", 2 ** next(flags_enum)),
            ("texts", "Texts", "Texts", "TEXT", 2 ** next(flags_enum)),
            ("textures", "Textures", "Textures", "TEXTURE_DATA", 2 ** next(flags_enum)),
            ("workspaces", "Workspaces", "Workspaces", "WORKSPACE", 2 ** next(flags_enum)),
        )
    )
asset_types.sort(key=lambda t: t[0])


def get_types(*args, **kwargs):
    return asset_types


def get_object_types():
    return (
        ("ARMATURE", "Armature", "Armature", "ARMATURE_DATA", 2 ** 1),
        ("CAMERA", "Camera", "Camera", "CAMERA_DATA", 2 ** 2),
        ("CURVE", "Curve", "Curve", "CURVE_DATA", 2 ** 3),
        ("EMPTY", "Empty", "Empty", "EMPTY_DATA", 2 ** 4),
        ("GPENCIL", "Grease Pencil", "Grease Pencil", "OUTLINER_DATA_GREASEPENCIL", 2 ** 5),
        ("LIGHT", "Light", "Light", "LIGHT", 2 ** 6),
        ("LIGHT_PROBE", "Light Probe", "Light Probe", "OUTLINER_DATA_LIGHTPROBE", 2 ** 7),
        ("LATTICE", "Lattice", "Lattice", "LATTICE_DATA", 2 ** 8),
        ("MESH", "Mesh", "Mesh", "MESH_DATA", 2 ** 9),
        ("META", "Metaball", "Metaball", "META_DATA", 2 ** 10),
        ("POINTCLOUD", "Point Cloud", "Point Cloud", "POINTCLOUD_DATA", 2 ** 11),
        ("SPEAKER", "Speaker", "Speaker", "OUTLINER_DATA_SPEAKER", 2 ** 12),
        ("SURFACE", "Surface", "Surface", "SURFACE_DATA", 2 ** 13),
        ("VOLUME", "Volume", "Volume", "VOLUME_DATA", 2 ** 14),
        ("FONT", "Text", "Text", "FONT_DATA", 2 ** 15),
    )


class FilterTypes(PropertyGroup):
    allow: BoolProperty(default=True)
    types_global_filter: BoolProperty(default=True, name="Filter By Type")
    types: EnumProperty(
        options={"ENUM_FLAG"},
        items=get_types(),
        default={"objects"},
    )
    types_object_filter: BoolProperty(default=False, name="Filter Objects")
    types_object: EnumProperty(
        options={"ENUM_FLAG"},
        items=get_object_types(),
        default={
            "CURVE",
            "MESH",
        },
    )

    def draw(self, layout):
        box = layout.box()

        row = box.row(align=True)
        row.prop(self, "types_global_filter", icon="FILTER")

        if self.types_global_filter:
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
