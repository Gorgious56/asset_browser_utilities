import bpy
from bpy.types import PropertyGroup
from bpy.props import BoolProperty, StringProperty, CollectionProperty

class FilterType(PropertyGroup):
    value: BoolProperty()
    icon: StringProperty()


class FilterTypes(PropertyGroup):
    items: CollectionProperty(type=FilterType)

    def init(self):
        if not self.items:
            for name, (value, icon) in {
                "Actions": (False, "ACTION"),
                "Materials": (False, "MATERIAL"),
                "Objects": (True, "OBJECT_DATA"),
                "Worlds": (False, "WORLD"),
            }.items():
                new = self.items.add()
                new.name = name
                new.value = value
                new.icon = icon
    
    def copy(self, other):
        self.items.clear()
        for item in other.items:
            new = self.items.add()
            new.value = item.value
            new.name = item.name
            new.icon = item.icon

    def draw(self, layout):        
        box = layout.box()
        box.label(text="Filter By Type", icon="FILTER")
        col = box.column(align=True)        
        for filter_type in self.items:
            col.prop(filter_type, "value", text=filter_type.name, toggle=True, icon=filter_type.icon)

    def populate(self, items):        
        for filter_type in self.items:
            if not filter_type.value:
                continue
            for item in getattr(bpy.data, filter_type.name.lower()):
                items.append(item)
