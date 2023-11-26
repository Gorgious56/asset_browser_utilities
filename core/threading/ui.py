import bpy


class ABUProgressProps(bpy.types.PropertyGroup):
    tasks_total: bpy.props.IntProperty(min=1)
    tasks_current: bpy.props.IntProperty()

    def init(self, tasks_total):
        self.tasks_total = tasks_total
        self.tasks_current = 0

    @property
    def factor(self):
        return self.tasks_current / self.tasks_total if self.tasks_total > 0 else -1

    def update_for_task_finished(self):
        self.tasks_current += 1


def register():
    bpy.types.WindowManager.abu_progress = bpy.props.PointerProperty(type=ABUProgressProps)


def unregister():
    del bpy.types.WindowManager.abu_progress
