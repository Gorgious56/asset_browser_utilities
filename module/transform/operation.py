from math import radians
from asset_browser_utilities.core.operator.prop import ObjectFilteredOperation
from mathutils import Vector, Euler
import bpy


def apply_transforms(assets, loc=False, rot=False, scale=False):
    if bpy.app.version >= (3, 2, 0):
        with bpy.context.temp_override(selected_editable_objects=[a for a in assets if hasattr(a, "matrix_world")]):
            bpy.ops.object.transform_apply(location=loc, rotation=rot, scale=scale)
    else:
        bpy.ops.object.transform_apply(
            {"selected_editable_objects": [a for a in assets if hasattr(a, "matrix_world")]},
            location=loc,
            rotation=rot,
            scale=scale,
        )


class ApplyTransformOperation(ObjectFilteredOperation):
    MAPPING = "APPLY_TRANSFORMS"
    LABEL = "Apply Transforms"
    DESCRIPTION = "Apply Location, Rotation, Scale"
    OPERATION = lambda assets: apply_transforms(assets, loc=True, rot=True, scale=True)


class ApplyLocationOperation(ObjectFilteredOperation):
    MAPPING = "APPLY_LOCATION"
    LABEL = "Apply Location"
    DESCRIPTION = "Apply Location"
    OPERATION = lambda assets: apply_transforms(assets, loc=True)


class ApplyRotationOperation(ObjectFilteredOperation):
    MAPPING = "APPLY_ROTATION"
    LABEL = "Apply Rotation"
    DESCRIPTION = "Apply Rotation"
    OPERATION = lambda assets: apply_transforms(assets, rot=True)


class ApplyScaleOperation(ObjectFilteredOperation):
    MAPPING = "APPLY_SCALE"
    LABEL = "Apply Scale"
    DESCRIPTION = "Apply Scale"
    OPERATION = lambda assets: apply_transforms(assets, scale=True)


class TranslateOperation(ObjectFilteredOperation):
    MAPPING = "TRANSLATE"
    LABEL = "Translate"
    DESCRIPTION = "Translate"
    OPERATION = lambda assets, vector: [
        setattr(a, "location", a.location + Vector(vector)) for a in assets if hasattr(a, "location")
    ]
    ATTRIBUTE = "vector_value"


class ScaleOperation(ObjectFilteredOperation):
    MAPPING = "SCALE"
    LABEL = "Scale"
    DESCRIPTION = "Scale"
    OPERATION = lambda assets, vector: [
        setattr(a, "scale", a.scale * Vector(vector)) for a in assets if hasattr(a, "scale")
    ]
    ATTRIBUTE = "vector_value"


def rotate_euler(obj, vector):
    vector = [radians(a) for a in vector]
    obj_euler = obj.rotation_euler
    obj_euler.rotate(Euler(vector))
    obj.rotation_euler = obj_euler


class RotateOperation(ObjectFilteredOperation):
    MAPPING = "ROTATE"
    LABEL = "Rotate"
    DESCRIPTION = "Rotate Euler Values as degrees in global coordinates"
    OPERATION = lambda assets, vector: [rotate_euler(a, vector) for a in assets if hasattr(a, "rotation_euler")]
    ATTRIBUTE = "vector_value"
    ATTRIBUTE_NAME = "Angles (Degrees)"
