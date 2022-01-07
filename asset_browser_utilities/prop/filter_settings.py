from bpy.types import PropertyGroup
from bpy.props import BoolProperty, PointerProperty

from asset_browser_utilities.prop.filter_type import FilterTypes
from asset_browser_utilities.prop.filter_name import FilterName

class AssetFilterSettings(PropertyGroup):
    filter_types: PointerProperty(type=FilterTypes)
    filter_name: PointerProperty(type=FilterName)
    filter_selection: BoolProperty(default=False)
    filter_selection_allow: BoolProperty()

    def init(self, filter_selection=False):
        self.filter_selection_allow = filter_selection
        self.filter_types.init()

    def query(self):
        assets = []

        self.filter_types.populate(assets)
        self.filter_name.filter(assets)
        if self.filter_selection:
            assets = [a for a in assets if a.select_get()]

        return assets

    def draw(self, layout):
        if self.filter_selection_allow:
            layout.prop(self, "filter_selection", text="Only Selected", icon="RESTRICT_SELECT_OFF")
        self.filter_types.draw(layout)
        self.filter_name.draw(layout)
