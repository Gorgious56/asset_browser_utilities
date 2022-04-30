from mathutils import Vector


class ApplyTransformOperation:
    MAPPING = "TRANSFORMS"
    LABEL = "Apply Transforms"
    DESCRIPTION = "Apply Location, Rotation, Scale"
    OPERATOR = True
    OPERATION = "object.transform_apply"
    ATTRIBUTE = "selected_editable_objects"
    ADDITIONAL_ATTRIBUTES = "location=True, rotation=True, scale=True"


class ApplyLocationOperation:
    MAPPING = "TRANSFORM_LOCATION"
    LABEL = "Apply Location"
    DESCRIPTION = "Apply Location"
    OPERATOR = True
    OPERATION = ApplyTransformOperation.OPERATION
    ATTRIBUTE = ApplyTransformOperation.ATTRIBUTE
    ADDITIONAL_ATTRIBUTES = "location=True, rotation=False, scale=False"


class ApplyRotationOperation:
    MAPPING = "TRANSFORM_ROTATION"
    LABEL = "Apply Rotation"
    DESCRIPTION = "Apply Rotation"
    OPERATOR = True
    OPERATION = ApplyTransformOperation.OPERATION
    ATTRIBUTE = ApplyTransformOperation.ATTRIBUTE
    ADDITIONAL_ATTRIBUTES = "location=False, rotation=True, scale=False"


class ApplyScaleOperation:
    MAPPING = "TRANSFORM_SCALE"
    LABEL = "Apply Scale"
    DESCRIPTION = "Apply Scale"
    OPERATOR = True
    OPERATION = ApplyTransformOperation.OPERATION
    ATTRIBUTE = ApplyTransformOperation.ATTRIBUTE
    ADDITIONAL_ATTRIBUTES = "location=False, rotation=False, scale=True"


class TranslateOperation:
    MAPPING = "TRANSLATE"
    LABEL = "Translate"
    DESCRIPTION = "Translate"
    OPERATOR = False
    OPERATION = lambda assets, vector: [setattr(a, "location", a.location + Vector(vector)) for a in assets]
    ATTRIBUTE = "vector_value"


class ScaleOperation:
    MAPPING = "SCALE"
    LABEL = "Scale"
    DESCRIPTION = "Scale"
    OPERATOR = False
    OPERATION = lambda assets, vector: [setattr(a, "scale", a.scale * Vector(vector)) for a in assets]
    ATTRIBUTE = "vector_value"
