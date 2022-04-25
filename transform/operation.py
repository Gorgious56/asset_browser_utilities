class ApplyTransformOperation:
    MAPPING = "TRANSFORMS"
    LABEL = "Apply Transforms"
    DESCRIPTION = "Apply Location, Rotation, Scale"
    OPERATION = "object.transform_apply"
    ATTRIBUTE = "selected_editable_objects"
    ADDITIONAL_ATTRIBUTES = "location=True, rotation=True, scale=True"


class ApplyLocationOperation:
    MAPPING = "TRANSFORM_LOCATION"
    LABEL = "Apply Location"
    DESCRIPTION = "Apply Location"
    OPERATION = ApplyTransformOperation.OPERATION
    ATTRIBUTE = ApplyTransformOperation.ATTRIBUTE
    ADDITIONAL_ATTRIBUTES = "location=True, rotation=False, scale=False"


class ApplyRotationOperation:
    MAPPING = "TRANSFORM_ROTATION"
    LABEL = "Apply Rotation"
    DESCRIPTION = "Apply Rotation"
    OPERATION = ApplyTransformOperation.OPERATION
    ATTRIBUTE = ApplyTransformOperation.ATTRIBUTE
    ADDITIONAL_ATTRIBUTES = "location=False, rotation=True, scale=False"


class ApplyScaleOperation:
    MAPPING = "TRANSFORM_SCALE"
    LABEL = "Apply Scale"
    DESCRIPTION = "Apply Scale"
    OPERATION = ApplyTransformOperation.OPERATION
    ATTRIBUTE = ApplyTransformOperation.ATTRIBUTE
    ADDITIONAL_ATTRIBUTES = "location=False, rotation=False, scale=True"
