from asset_browser_utilities.core.cache.tool import get_current_operator_properties, get_from_cache
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.module.custom_property.tool import copy_prop
from asset_browser_utilities.module.asset.prop import SelectedAssetFiles


class AssetDataCopyBatchExecute(BatchExecute):
    def do_on_asset(self, asset):
        operator_properties = get_current_operator_properties()
        active_asset = get_from_cache(SelectedAssetFiles).active_asset
        if asset == active_asset:
            return
        asset_data_source = active_asset.asset_data
        asset_data_target = asset.asset_data
        log_data = []
        if operator_properties.tags:
            tags_source = asset_data_target.tags
            for tag in asset_data_source.tags:
                tags_source.new(name=tag.name, skip_if_exists=True)
            log_data.append("tags")
        if operator_properties.custom_properties:
            for prop_name in asset_data_source.keys():
                copy_prop(asset_data_source, asset_data_target, prop_name)
            log_data.append("custom properties")
        if operator_properties.preview:
            source_preview = active_asset.preview
            if source_preview is not None:
                asset_preview = asset.preview
                asset_preview.image_size = source_preview.image_size
                asset_preview.image_pixels.foreach_set(source_preview.image_pixels)
                log_data.append("preview")
        if operator_properties.catalog:
            asset_data_target.catalog_id = asset_data_source.catalog_id
            log_data.append("catalog")
        if operator_properties.author:
            asset_data_target.author = asset_data_source.author
            log_data.append("author")
        if operator_properties.description:
            asset_data_target.description = asset_data_source.description
            log_data.append("description")
        props = ", ".join(log_data)
        Logger.display(f"Copied {props} from '{repr(active_asset)}' to '{repr(asset)}'")

        super().do_on_asset(asset)


class AssetDataCopyOperatorProperties(PropertyGroup):
    tags: BoolProperty(name="Tags")
    custom_properties: BoolProperty(name="Custom Properties")
    preview: BoolProperty(name="Preview")
    catalog: BoolProperty(name="Catalog")
    author: BoolProperty(name="Author")
    description: BoolProperty(name="Description")

    def draw(self, layout, context=None):
        box = layout.box()
        box.label(text="Copy These Properties From Active Asset")
        box.prop(self, "tags", icon="BOOKMARKS")
        box.prop(self, "custom_properties", icon="PROPERTIES")
        box.prop(self, "preview", icon="SEQ_PREVIEW")
        box.prop(self, "catalog", icon="OUTLINER_COLLECTION")
        box.prop(self, "author", icon="USER")
        box.prop(self, "description", icon="FILE_TEXT")


class ABU_OT_asset_data_copy(Operator, BatchFolderOperator):
    ui_library = LibraryType.FileCurrent.value
    bl_idname = "abu.asset_data_copy"
    bl_label = "Copy Data From Active"

    operator_settings: PointerProperty(type=AssetDataCopyOperatorProperties)
    logic_class = AssetDataCopyBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
