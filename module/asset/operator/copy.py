import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps

from asset_browser_utilities.module.asset.prop import SelectedAssetRepresentations
from asset_browser_utilities.module.tag.prop import ASSET_TAG_UUID_PREFIX


class AssetDataCopyOperatorProperties(PropertyGroup, BaseOperatorProps):
    tags: BoolProperty(name="Tags")
    preview: BoolProperty(name="Preview")
    catalog: BoolProperty(name="Catalog")
    author: BoolProperty(name="Author")
    description: BoolProperty(name="Description")
    license: BoolProperty(name="License")
    copyright: BoolProperty(name="Copyright")

    def draw(self, layout, context=None):
        box = layout.box()
        box.label(text="Copy These Properties From Active Asset")
        box.prop(self, "tags", icon="BOOKMARKS")
        box.prop(self, "preview", icon="SEQ_PREVIEW")
        box.prop(self, "catalog", icon="OUTLINER_COLLECTION")
        box.prop(self, "author", icon="USER")
        box.prop(self, "description", icon="FILE_TEXT")
        box.prop(self, "license", icon="FAKE_USER_OFF")
        box.prop(self, "copyright", icon="COPY_ID")

    def run_in_file(self, attributes=None):
        if not get_from_cache(SelectedAssetRepresentations).active_asset.is_local:
            return
        super().run_in_file(attributes)

    def run_on_asset(self, asset):
        active_asset_representation = get_from_cache(SelectedAssetRepresentations).active_asset
        active_asset = getattr(bpy.data, active_asset_representation.directory)[active_asset_representation.name]
        if asset == active_asset:
            return False
        asset_data_source = active_asset.asset_data
        asset_data_target = asset.asset_data
        log_data = []
        if self.tags:
            tags_source = asset_data_target.tags
            for tag in asset_data_source.tags:
                if tag.name.startswith(ASSET_TAG_UUID_PREFIX):
                    continue
                tags_source.new(name=tag.name, skip_if_exists=True)
            log_data.append("tags")
        if self.preview:
            source_preview = active_asset.preview
            if source_preview is not None and asset.preview is not None:
                asset_preview = asset.preview
                asset_preview.image_size = source_preview.image_size
                asset_preview.image_pixels.foreach_set(source_preview.image_pixels)
                log_data.append("preview")
        if self.catalog:
            asset_data_target.catalog_id = asset_data_source.catalog_id
            log_data.append("catalog")
        if self.license:
            asset_data_target.license = asset_data_source.license
            log_data.append("license")
        if self.copyright:
            asset_data_target.copyright = asset_data_source.copyright
            log_data.append("copyright")
        if self.author:
            asset_data_target.author = asset_data_source.author
            log_data.append("author")
        if self.description:
            asset_data_target.description = asset_data_source.description
            log_data.append("description")
        props = ", ".join(log_data)
        Logger.display(f"{bpy.data.filepath} : Copied {props} from '{repr(active_asset)}' to '{repr(asset)}'")


class ABU_OT_asset_data_copy(Operator, BatchFolderOperator):
    ui_library = LibraryType.FileCurrent.value
    bl_idname = "abu.asset_data_copy"
    bl_label = "Copy Data From Active"

    operator_settings: PointerProperty(type=AssetDataCopyOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
