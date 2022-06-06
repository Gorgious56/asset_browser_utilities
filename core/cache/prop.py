from asset_browser_utilities.catalog.operator.move_from_a_to_b import CatalogMoveFromAToBOperatorProperties
from asset_browser_utilities.catalog.operator.move_to import CatalogMoveOperatorProperties
from asset_browser_utilities.catalog.operator.remove_from import CatalogRemoveFromOperatorProperties
from asset_browser_utilities.core.operator.operation import OperationSettings
from asset_browser_utilities.core.operator.prop import CurrentOperatorProperty
from asset_browser_utilities.preview.operator.generate import PreviewGenerateOperatorProperties
from bpy.types import PropertyGroup
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.filter.main import AssetFilterSettings
from asset_browser_utilities.library.prop import LibraryExportSettings
from asset_browser_utilities.catalog.prop import CatalogExportSettings

from asset_browser_utilities.asset.operator.mark import OperatorProperties as MarkOperatorProperties
from asset_browser_utilities.asset.export.operator import OperatorProperties as ExportOperatorProperties
from asset_browser_utilities.asset.operator.copy import OperatorProperties as CopyOperatorProperties
from asset_browser_utilities.tag.operator.tool import AddOrRemoveTagsOperatorProperties
from asset_browser_utilities.tag.operator.add_smart import OperatorProperties as AddSmartTagOperatorProperties
from asset_browser_utilities.custom_property.operator.set import SetCustomPropertyOperatorProperties
from asset_browser_utilities.custom_property.operator.remove import RemoveCustomPropertyOperatorProperties
from asset_browser_utilities.asset.prop import SelectedAssetFiles


class Cache(PropertyGroup):
    library_settings: PointerProperty(type=LibraryExportSettings)
    operation_settings: PointerProperty(type=OperationSettings)
    asset_filter_settings: PointerProperty(type=AssetFilterSettings)
    catalog_settings: PointerProperty(type=CatalogExportSettings)
    
    current_op: PointerProperty(type=CurrentOperatorProperty)
    mark_op: PointerProperty(type=MarkOperatorProperties)
    copy_op: PointerProperty(type=CopyOperatorProperties)
    export_op: PointerProperty(type=ExportOperatorProperties)
    smart_tag_op: PointerProperty(type=AddSmartTagOperatorProperties)
    add_or_remove_tag_op: PointerProperty(type=AddOrRemoveTagsOperatorProperties)
    custom_prop_set_op: PointerProperty(type=SetCustomPropertyOperatorProperties)
    custom_prop_remove_op: PointerProperty(type=RemoveCustomPropertyOperatorProperties)
    preview_generate_op: PointerProperty(type=PreviewGenerateOperatorProperties)
    catalog_move_from_a_to_b_op: PointerProperty(type=CatalogMoveFromAToBOperatorProperties)
    catalog_move_op: PointerProperty(type=CatalogMoveOperatorProperties)
    catalog_remove_op: PointerProperty(type=CatalogRemoveFromOperatorProperties)
    
    selected_assets: PointerProperty(type=SelectedAssetFiles)

    show: BoolProperty()

    def get(self, _type):
        for prop_name in self.__annotations__:
            prop = getattr(self, prop_name)
            if isinstance(prop, _type):
                return prop
    
    def draw(self, layout, context, header=None, rename=False):
        if header is None:
            header = self.name
        row = layout.row(align=True)
        if rename:
            row.prop(self, "name")
        row.prop(self, "show", toggle=True, text=header)
        if self.show:
            for attr in self.__annotations__:
                default_setting = getattr(self, attr)
                if hasattr(default_setting, "draw"):
                    default_setting.draw(layout, context)
        
