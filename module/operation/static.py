from asset_browser_utilities.module.transform.operation import (
    ApplyTransformOperation,
    ApplyLocationOperation,
    ApplyScaleOperation,
    ApplyRotationOperation,
    TranslateOperation,
    ScaleOperation,
    RotateOperation,
)
from asset_browser_utilities.module.mesh.operation import DecimateOperation
from asset_browser_utilities.module.asset.operation import (
    RenameAssetOperation,
    RenameDataOperation,
    RenameMaterialOperation,
)


class NONE_OPERATION:
    MAPPING = "NONE"
    LABEL = "None"
    DESCRIPTION = "No Operation"


OPERATION_MAPPING = {
    NONE_OPERATION.MAPPING: NONE_OPERATION,
    ApplyTransformOperation.MAPPING: ApplyTransformOperation,
    ApplyLocationOperation.MAPPING: ApplyLocationOperation,
    ApplyRotationOperation.MAPPING: ApplyRotationOperation,
    ApplyScaleOperation.MAPPING: ApplyScaleOperation,
    TranslateOperation.MAPPING: TranslateOperation,
    ScaleOperation.MAPPING: ScaleOperation,
    RotateOperation.MAPPING: RotateOperation,
    DecimateOperation.MAPPING: DecimateOperation,
    RenameAssetOperation.MAPPING: RenameAssetOperation,
    RenameDataOperation.MAPPING: RenameDataOperation,
    RenameMaterialOperation.MAPPING: RenameMaterialOperation,
}
