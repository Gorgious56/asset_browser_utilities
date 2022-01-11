from bpy.types import PropertyGroup
from bpy.props import BoolProperty, StringProperty, CollectionProperty

from asset_browser_utilities.helper.prop import copy_simple_property_group


class FilterType(PropertyGroup):
    name: StringProperty()
    value: BoolProperty()
    icon: StringProperty()


class FilterTypes(PropertyGroup):
    items: CollectionProperty(type=FilterType)
    MAPPING = {
        "actions": {
            "icon": "ACTION",
        },
        "materials": {
            "icon": "MATERIAL",
        },
        "objects": {
            "value": True,
            "icon": "OBJECT_DATA",
        },
        "worlds": {
            "icon": "WORLD",
        },
    }

    def init(self):
        if not self.items:
            for name, data in self.MAPPING.items():
                new = self.items.add()
                new.name = name
                for data_name, data_value in data.items():
                    setattr(new, data_name, data_value)

    def copy(self, other):
        self.items.clear()
        for source in other.items:
            target = self.items.add()
            copy_simple_property_group(source, target)

    def draw(self, layout):
        box = layout.box()
        box.label(text="Filter By Type", icon="FILTER")
        col = box.column(align=True)
        for filter_type in self.items:
            col.prop(filter_type, "value", text=filter_type.name.title(), toggle=True, icon=filter_type.icon)
