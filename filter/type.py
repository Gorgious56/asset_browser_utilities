from bpy.types import PropertyGroup
from bpy.props import BoolProperty, StringProperty, CollectionProperty

from asset_browser_utilities.core.helper import copy_simple_property_group


class FilterType(PropertyGroup):
    name: StringProperty()
    value: BoolProperty()
    icon: StringProperty()


class FilterTypes(PropertyGroup):
    items: CollectionProperty(type=FilterType)
    items_object: CollectionProperty(type=FilterType)
    items_object_filter: BoolProperty(default=False)
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
    MAPPING_OBJECT = {
        "ARMATURE": {
            "icon": "ARMATURE_DATA",
        },
        "CAMERA": {
            "icon": "CAMERA_DATA",
        },
        "CURVE": {
            "icon": "CURVE_DATA",
            "value": True,
        },
        "EMPTY": {
            "icon": "EMPTY_DATA",
        },
        "GREASEPENCIL": {
            "icon": "OUTLINER_DATA_GREASEPENCIL",
        },
        "HAIR": {
            "icon": "HAIR_DATA",
        },
        "LIGHT": {
            "icon": "LIGHT",
        },
        "LIGHT_PROBE": {
            "icon": "OUTLINER_DATA_LIGHTPROBE",
        },
        "LATTICE": {
            "icon": "LATTICE_DATA",
        },
        "MESH": {
            "icon": "MESH_DATA",
            "value": True,
        },
        "META": {
            "icon": "META_DATA",
        },
        "POINTCLOUD": {
            "icon": "POINTCLOUD_DATA",
        },
        "SPEAKER": {
            "icon": "OUTLINER_DATA_SPEAKER",
        },
        "SURFACE": {
            "icon": "SURFACE_DATA",
        },
        "VOLUME": {
            "icon": "VOLUME_DATA",
        },
        "FONT": {
            "icon": "FONT_DATA",
        },
    }

    def init(self):
        for container, mapping in zip((self.items, self.items_object), (self.MAPPING, self.MAPPING_OBJECT)):
            if not container:
                for name, data in mapping.items():
                    new = container.add()
                    new.name = name
                    for data_name, data_value in data.items():
                        setattr(new, data_name, data_value)

    def copy(self, other):
        copy_simple_property_group(other, self)
        for container_name in ("items", "items_object"):
            container_self = getattr(self, container_name)
            container_self.clear()
            for source in getattr(other, container_name):
                target = container_self.add()
                copy_simple_property_group(source, target)

    def draw(self, layout):
        box = layout.box()
        box.label(text="Filter By Type", icon="FILTER")
        col = box.column(align=True)
        for filter_type in self.items:
            row = col.row(align=True)
            row.prop(filter_type, "value", text=filter_type.name.title(), toggle=True, icon=filter_type.icon)
            if filter_type.name == "objects":
                row.prop(self, "items_object_filter", text="", icon="FILTER")
                if self.items_object_filter:
                    box_object = col.box()
                    col_object = box_object.column(align=True)
                    for filter_type_obj in self.items_object:
                        col_object.prop(
                            filter_type_obj,
                            "value",
                            text=filter_type_obj.name.title(),
                            toggle=True,
                            icon=filter_type_obj.icon,
                        )
