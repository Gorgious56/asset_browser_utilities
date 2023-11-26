import string

import bpy
from bpy.types import PropertyGroup
from bpy.props import IntProperty, PointerProperty

ALPHABET = string.ascii_lowercase + string.digits


class StringPropertyCollection(PropertyGroup):
    pass


class IntPropertyCollection(PropertyGroup):
    value: IntProperty(min=0)


class AnyID(PropertyGroup):
    Action: PointerProperty(type=bpy.types.Action)
    Armature: PointerProperty(type=bpy.types.Armature)
    Brush: PointerProperty(type=bpy.types.Brush)
    Camera: PointerProperty(type=bpy.types.Camera)
    CacheFile: PointerProperty(type=bpy.types.CacheFile)
    Collection: PointerProperty(type=bpy.types.Collection)
    Curve: PointerProperty(type=bpy.types.Curve)
    VectorFont: PointerProperty(type=bpy.types.VectorFont)
    GreasePencil: PointerProperty(type=bpy.types.GreasePencil)
    Image: PointerProperty(type=bpy.types.Image)
    Key: PointerProperty(type=bpy.types.Key)
    Light: PointerProperty(type=bpy.types.Light)
    Library: PointerProperty(type=bpy.types.Library)
    FreestyleLineStyle: PointerProperty(type=bpy.types.FreestyleLineStyle)
    Lattice: PointerProperty(type=bpy.types.Lattice)
    Mask: PointerProperty(type=bpy.types.Mask)
    Material: PointerProperty(type=bpy.types.Material)
    Mesh: PointerProperty(type=bpy.types.Mesh)
    MovieClip: PointerProperty(type=bpy.types.MovieClip)
    NodeTree: PointerProperty(type=bpy.types.NodeTree)
    Object: PointerProperty(type=bpy.types.Object)
    PaintCurve: PointerProperty(type=bpy.types.PaintCurve)
    Palette: PointerProperty(type=bpy.types.Palette)
    ParticleSettings: PointerProperty(type=bpy.types.ParticleSettings)
    LightProbe: PointerProperty(type=bpy.types.LightProbe)
    Scene: PointerProperty(type=bpy.types.Scene)
    Sound: PointerProperty(type=bpy.types.Sound)
    Speaker: PointerProperty(type=bpy.types.Speaker)
    Text: PointerProperty(type=bpy.types.Text)
    Texture: PointerProperty(type=bpy.types.Texture)
    Volume: PointerProperty(type=bpy.types.Volume)
    WindowManager: PointerProperty(type=bpy.types.WindowManager)
    World: PointerProperty(type=bpy.types.World)
    WorkSpace: PointerProperty(type=bpy.types.WorkSpace)
    id_type: bpy.props.EnumProperty(
        items=[
            ("Action", "Action", "", "ACTION", 1),
            ("Armature", "Armature", "", "ARMATURE_DATA", 2),
            ("Brush", "Brush", "", "BRUSH_DATA", 3),
            ("Camera", "Camera", "", "CAMERA_DATA", 4),
            ("CacheFile", "Armature", "", "FILE", 5),
            ("Collection", "Collection", "", "OUTLINER_COLLECTION", 6),
            ("Curve", "Curve", "", "OUTLINER_DATA_CURVE", 7),
            ("VectorFont", "Font", "", "FONT_DATA", 8),
            ("GreasePencil", "Grease Pencil", "", "GREASEPENCIL", 9),
            ("Image", "Image", "", "IMAGE_DATA", 10),
            ("Key", "Key", "", "SHAPEKEY_DATA", 11),
            ("Light", "Light", "", "LIGHT", 12),
            ("Library", "Library", "", "LIBRARY_DATA_DIRECT", 13),
            ("FreestyleLineStyle", "Line Style", "", "LINE_DATA", 14),
            ("Lattice", "Lattice", "", "LATTICE_DATA", 15),
            ("Mask", "Mask", "", "MOD_MASK", 16),
            ("Material", "Material", "", "MATERIAL", 17),
            ("Mesh", "Mesh", "", "MESH_DATA", 18),
            ("MovieClip", "Movie Clip", "", "TRACKER", 19),
            ("NodeTree", "Node Tree", "", "NODETREE", 20),
            ("Object", "Object", "", "OBJECT_DATA", 21),
            ("PaintCurve", "Paint Curve", "", "CURVE_BEZCURVE", 22),
            ("Palette", "Palette", "", "COLOR", 23),
            ("ParticleSettings", "Particle", "", "PARTICLES", 24),
            ("LightProbe", "Light Probe", "", "LIGHTPROBE_CUBEMAP", 25),
            ("Scene", "Scene", "", "SCENE_DATA", 26),
            ("Sound", "Sound", "", "SOUND", 28),
            ("Speaker", "Speaker", "", "SPEAKER", 29),
            ("Text", "Text", "", "TEXT", 30),
            ("Texture", "Texture", "", "TEXTURE", 31),
            ("Volume", "Volume", "", "VOLUME_DATA", 32),
            ("WindowManager", "Window Manager", "", "WINDOW", 33),
            ("World", "World", "", "WORLD", 34),
            ("WorkSpace", "Workspace", "", "WORKSPACE", 35),
        ],
        default="Object",
        name="ID Type",
    )

    def draw(self, layout, context=None):
        split = layout.split(factor=0.1, align=True)
        split.prop(self, "id_type", text="", icon_only=True)
        split.prop(self, self.id_type, text="")

    def get(self):
        return getattr(self, self.id_type)

    def set(self, value):
        class_name = value.__class__.__name__
        if "nodetree" in class_name.lower():
            class_name = "NodeTree"
        elif "texture" in class_name.lower():
            class_name = "Texture"
        self.id_type = class_name
        setattr(self, self.id_type, value)
