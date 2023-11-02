import calendar
from datetime import datetime, timedelta
from bpy.types import PropertyGroup, Operator
from bpy.props import PointerProperty, BoolProperty, EnumProperty, IntProperty


class ABU_OT_datetime_update(Operator):
    bl_idname = "abu.datetime_update"
    bl_label = "Update Date"
    bl_options = {"UNDO", "INTERNAL"}

    year: IntProperty()
    month: IntProperty()
    day: IntProperty()
    hour: IntProperty()
    minute: IntProperty()
    second: IntProperty()

    def execute(self, context):
        props = context.datetime
        if self.month > 12:
            self.year += 1
            self.month = 1
        elif self.month <= 0:
            self.year -= 1
            self.month = 12

        if self.day:
            props.day = self.day
        if self.month:
            props.month = self.month
        if self.year:
            props.year = self.year
        if self.hour:
            props.hour = self.hour
        if self.minute:
            props.minute = self.minute
        if self.second:
            props.second = self.second

        return {"FINISHED"}


class DateTime(PropertyGroup):
    year: IntProperty(min=1, soft_min=1900, soft_max=2100, max=9999, default=datetime.now().year)
    month: IntProperty(min=1, max=12, default=datetime.now().month)
    day: IntProperty(min=1, max=31, default=datetime.now().day)
    hour: IntProperty(min=0, max=23, default=datetime.now().hour)
    minute: IntProperty(min=0, max=59, default=datetime.now().minute)
    second: IntProperty(min=0, max=59, default=datetime.now().second)

    def to_datetime(self):
        return datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)

    def __repr__(self) -> str:
        return self.name + " " + self.to_datetime.__repr__()

    def draw(self, layout, context):
        layout.context_pointer_set("datetime", self)
        props = self
        day = props.day
        month = props.month
        year = props.year
        now = datetime.now()

        layout = layout.box()
        layout.label(text=self.name)

        split = layout.split(factor=0.1)
        self.change_day_op(
            split,
            "",
            {
                "month": now.month,
                "year": now.year,
                "day": now.day,
                "hour": now.hour,
                "minute": now.minute,
                "second": now.second,
            },
            icon="RECOVER_LAST",
        )
        header = split.split(factor=0.7)

        row = header.row()
        row.label(text=calendar.month_name[month].upper())
        row.prop(props, "year", text="", emboss=False)

        row = header.row(align=True)
        for txt, inc in zip(("<", ">"), (-1, 1)):
            self.change_day_op(row, txt, {"month": month + inc, "year": year})

        date = datetime(year, month, 1)

        weekday = date.weekday()

        for r in range(7):
            new_date = None
            row = layout.row(align=True)
            for c in range(8):
                col = row.column(align=True)
                label = ""
                if c == 0:
                    if r == 0:
                        label = "#"
                    else:
                        label = "w" + str((date + timedelta(days=(r - 1) * 7)).isocalendar()[1])
                elif r == 0:
                    label = calendar.day_name[c - 1][0:3].upper()
                else:
                    new_date = date + timedelta(days=c - 1 + (r - 1) * 7 - weekday)
                    label = new_date.day
                if isinstance(label, int) and new_date:
                    self.change_day_op(
                        col,
                        str(label),
                        {
                            "day": label,
                            "month": new_date.month,
                            "year": new_date.year,
                        },
                        emboss=new_date.month == month,
                        depress=(new_date.day == day and new_date.month == month and new_date.year == year),
                    )
                else:
                    col.label(text=str(label))
        layout.separator()
        row = layout.row()
        for p, t in zip(("hour", "minute", "second"), (":", "''", "'")):
            split = row.split(factor=0.8)
            split.prop(props, p, text="")
            split.label(text=t)

    @staticmethod
    def change_day_op(layout, txt, op_settings, emboss=True, depress=False, icon=None):
        if icon:
            op = layout.operator(ABU_OT_datetime_update.bl_idname, text=txt, emboss=emboss, depress=depress, icon=icon)
        else:
            op = layout.operator(ABU_OT_datetime_update.bl_idname, text=txt, emboss=emboss, depress=depress)

        for op_prop, op_value in op_settings.items():
            setattr(op, op_prop, op_value)


class FilterDate(PropertyGroup):
    active: BoolProperty()
    before: PointerProperty(type=DateTime, name="Before")
    after: PointerProperty(type=DateTime, name="After")

    mode: EnumProperty(
        items=[
            ("BEFORE", "Before", "Operate on files last modified before date"),
            ("AFTER", "After", "Operate on files last modified after date"),
            ("BETWEEN", "Between", "Operate on files last modified between two dates"),
        ],
        default="AFTER",
    )

    def init(self):
        self.before.name = "Before"
        self.after.name = "After"

    def draw(self, layout, context=None):
        box = layout.box()
        box.prop(self, "active", icon="FILTER", text="Filter by Date")
        if self.active:
            box.prop(self, "mode", expand=True)
            if self.mode in ("BEFORE", "BETWEEN"):
                self.before.draw(box, context)
            if self.mode in ("AFTER", "BETWEEN"):
                self.after.draw(box, context)

    def filter(self, timestamp_test):
        if not self.active:
            return True
        datetime_test = datetime.fromtimestamp(timestamp_test)
        return FilterDate.filter_static(datetime_test, self.mode, self.before, self.after)

    @staticmethod
    def filter_static(datetime_test, mode, before, after):
        if mode in ("BEFORE", "BETWEEN"):
            if datetime_test > before.to_datetime():
                return False
        if mode in ("AFTER", "BETWEEN"):
            if datetime_test < after.to_datetime():
                return False
        return True
