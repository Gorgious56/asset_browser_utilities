import re

import bpy
from bpy_extras import (
    asset_utils,
)

url_pattern = r'https?://[^\s<>"\'\(\)]+'


class ASSETBROWSER_PT_metadata_utilities(asset_utils.AssetMetaDataPanel, bpy.types.Panel):
    bl_label = "Utilities"

    def draw(self, context):
        layout = self.layout
        asset = context.asset
        metadata = asset.metadata
        urls_desc = re.findall(url_pattern, metadata.description)
        urls_author = re.findall(url_pattern, metadata.author)
        urls_license = re.findall(url_pattern, metadata.license)
        urls_copyright = re.findall(url_pattern, metadata.copyright)
        for url in urls_desc + urls_author + urls_license + urls_copyright:
            op = layout.operator("abu.open_url", text=url, icon="URL")
            op.url = url
