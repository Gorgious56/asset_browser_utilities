import bpy
from bpy.types import PropertyGroup
from bpy.props import BoolProperty, IntProperty, CollectionProperty, EnumProperty


class TagName(PropertyGroup):
    def is_empty(self):
        return self.name == ""


def set_shown_tags(self, value):
    # This is extremely hacky but emulates dynamically adding or removing tags
    if value == 1:
        self.shown_tags += 1
        if self.shown_tags >= len(self.items):
            self.shown_tags = len(self.items)
    if value == 2:
        self.shown_tags -= 1


class TagCollection(PropertyGroup):
    items: CollectionProperty(type=TagName)
    shown_tags: IntProperty(default=1, min=1)
    tag_internal: EnumProperty(
        items=(
            ("NONE",) * 3,
            ("+",) * 3,
            ("-",) * 3,
        ),
        set=set_shown_tags,
    )

    remove_all: BoolProperty(name="Remove All", default=False)
    add: BoolProperty()

    def init(self, tags: int = 10):
        # We semi-hardcode number of tags here
        while len(self.items) < tags:
            self.items.add()

    def draw(self, layout):
        box = layout.box()
        row = box.row()
        split = row.split(factor=0.2)
        split.label(text="Tags")
        row = split.row(align=True)
        row.prop_enum(self, "tag_internal", value="+", icon="ADD", text="")
        row.prop_enum(self, "tag_internal", value="-", icon="REMOVE", text="")
        row.enabled = not self.remove_all
        if not self.add:
            split.prop(self, "remove_all", toggle=True, icon="TRASH")
        if not self.remove_all:
            col = box.column(align=True)
            for i, tag in enumerate(self.items):
                if i < self.shown_tags:
                    col.prop(tag, "name", text=f"Tag {i + 1}")
