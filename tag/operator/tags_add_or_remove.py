from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
from bpy.props import StringProperty, PointerProperty

from asset_browser_utilities.tag.tag_collection import TagCollection
from asset_browser_utilities.file.path import open_file_if_different_from_current

from asset_browser_utilities.file.save import save_file_as, save_if_possible_and_necessary
from asset_browser_utilities.core.operator.helper import FilterLibraryOperator


class BatchAddOrRemoveTagsOperator:
    filter_glob: StringProperty(
        default="*.blend",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    tag_collection: PointerProperty(type=TagCollection)
    MAX_TAGS = 10

    def execute(self, context):
        save_if_possible_and_necessary()
        blends = self.library_settings.get_blend_files(self.filepath)
        for blend in blends:
            self.execute_on_blend(blend)
        return {"FINISHED"}

    def execute_on_blend(self, filepath):
        open_file_if_different_from_current(filepath)
        objs = self.asset_filter_settings.get_objects_that_satisfy_filters()
        for obj in objs:
            self.execute_on_obj(obj)
        save_file_as(str(filepath), remove_backup=self.library_settings.remove_backup)

    def execute_on_obj(self, obj):
        asset = obj.asset_data
        asset_tags = asset.tags
        self.execute_tags(asset_tags)

    def draw(self, context):
        layout = self.layout
        self.library_settings.draw(layout)
        self.tag_collection.draw(layout)
        self.asset_filter_settings.draw(layout)


class ASSET_OT_batch_add_tags(Operator, ImportHelper, BatchAddOrRemoveTagsOperator, FilterLibraryOperator):
    "Add tags"
    bl_idname = "asset.batch_add_tags"
    bl_label = "Add tags"

    def invoke(self, context, event):
        self.tag_collection.add = True
        self.tag_collection.init(tags=self.MAX_TAGS)
        return self._invoke(context, filter_assets=True)

    def execute_tags(self, asset_tags):
        existing_tags = [tag.name for tag in asset_tags]
        for tag in self.tag_collection.items:
            if tag.is_empty() or tag.name in existing_tags:
                continue
            asset_tags.new(tag.name)


class ASSET_OT_batch_remove_tags(Operator, ImportHelper, BatchAddOrRemoveTagsOperator, FilterLibraryOperator):
    "Remove tags"
    bl_idname = "asset.batch_remove_tags"
    bl_label = "Remove tags"

    def invoke(self, context, event):
        self.tag_collection.add = False
        self.tag_collection.init(tags=self.MAX_TAGS)
        return self._invoke(context, filter_assets=True)

    def execute_tags(self, asset_tags):
        tags_to_remove = self.get_tags_to_remove(asset_tags)
        self.remove_tags(asset_tags, tags_to_remove)

    def get_tags_to_remove(self, asset_tags):
        if self.tag_collection.remove_all:
            return [tag.name for tag in asset_tags]
        else:
            return [tag.name for tag in self.tag_collection.items if tag.name != ""]

    def remove_tags(self, asset_tags, tags_to_remove):
        for i in range(len(asset_tags) - 1, -1, -1):
            if asset_tags[i].name in tags_to_remove:
                asset_tags.remove(asset_tags[i])
