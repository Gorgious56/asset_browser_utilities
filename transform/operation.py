class TransformApplyOperation:
    MAPPING = "TRANSFORMS"
    LABEL = "Apply Transforms"
    DESCRIPTION = "Apply Location, Rotation, Scale"
    OPERATION = "object.transform_apply"
    ATTRIBUTE = "selected_editable_objects"
    ADDITIONAL_ATTRIBUTES = "location=True, rotation=True, scale=True"


class LocationApplyOperation:
    MAPPING = "TRANSFORM_LOCATION"
    LABEL = "Apply Location"
    DESCRIPTION = "Apply Location"
    OPERATION = TransformApplyOperation.OPERATION
    ATTRIBUTE = TransformApplyOperation.ATTRIBUTE
    ADDITIONAL_ATTRIBUTES = "location=True, rotation=False, scale=False"


class RotationApplyOperation:
    MAPPING = "TRANSFORM_ROTATION"
    LABEL = "Apply Rotation"
    DESCRIPTION = "Apply Rotation"
    OPERATION = TransformApplyOperation.OPERATION
    ATTRIBUTE = TransformApplyOperation.ATTRIBUTE
    ADDITIONAL_ATTRIBUTES = "location=False, rotation=True, scale=False"


class ScaleApplyOperation:
    MAPPING = "TRANSFORM_SCALE"
    LABEL = "Apply Scale"
    DESCRIPTION = "Apply Scale"
    OPERATION = TransformApplyOperation.OPERATION
    ATTRIBUTE = TransformApplyOperation.ATTRIBUTE
    ADDITIONAL_ATTRIBUTES = "location=False, rotation=False, scale=True"
