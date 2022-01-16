import numpy as np


def is_preview_generated(asset):
    preview = asset.preview
    if not preview:
        asset.asset_generate_preview()
    arr = np.zeros((preview.image_size[0] * preview.image_size[1]) * 4, dtype=np.float32)
    preview.image_pixels_float.foreach_get(arr)
    return np.any((arr != 0))
