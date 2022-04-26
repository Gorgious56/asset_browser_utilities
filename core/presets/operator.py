from bpy.types import Operator
from bpy.props import IntProperty

from asset_browser_utilities.core.preferences.tool import get_preferences


class ABU_OT_presets_add_or_remove(Operator):
    bl_idname = "abu.presets_add_or_remove"
    bl_label = "Add Preset"
    index: IntProperty()

    def execute(self, context):
        presets = get_preferences(context).presets
        if self.index < 0:
            new = presets.add()
            new.name = "New Preset"
            new.asset_filter_settings.filter_selection.allow = True
            new.asset_filter_settings.filter_catalog.allow = True
        else:
            try:
                presets.remove(self.index)
            except IndexError:
                pass
        return {"FINISHED"}
