from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, PointerProperty
from bpy.types import Operator

from asset_browser_utilities.filter.main import AssetFilterSettings
from asset_browser_utilities.library.path import LibraryExportSettings
from asset_browser_utilities.core.preferences.helper import write_to_cache, get_from_cache
from asset_browser_utilities.file.path import (
    get_blend_files,
    save_if_possible_and_necessary,
)
from asset_browser_utilities.core.operator.helper import FilterLibraryOperator


class ASSET_OT_batch_generate_previews(Operator, ImportHelper, FilterLibraryOperator):
    bl_idname = "asset.batch_generate_previews"
    bl_label = "Batch Generate Previews"

    def invoke(self, context, event):
        return self._invoke(context)
