import os
from pathlib import Path
import bpy
from mathutils import Matrix, Vector
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty
from bpy.types import Operator

from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps
from asset_browser_utilities.core.library.prop import LibraryExportSettings, LibraryType
from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.operator.tool import BatchFolderOperator
from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.file.save import save_file_as


import_ops_from_file_extension = {
    "gltf": bpy.ops.import_scene.gltf,
    "fbx": bpy.ops.import_scene.fbx,
    "stl": bpy.ops.wm.stl_import,
    "obj": bpy.ops.wm.obj_import,
}


class StrProperty(PropertyGroup):
    pass


class ModelConvertOperatorProperties(PropertyGroup, BaseOperatorProps):
    file_extension: bpy.props.EnumProperty(
        items=(
            ("gltf",) * 3,
            ("fbx",) * 3,
            ("stl",) * 3,
            ("obj",) * 3,
        ),
        name="File Type",
    )  # type: ignore
    target_faces: IntProperty(
        name="Target Faces",
        description="The decimate modifier will give this number of polygons (0 keeps the same number of faces)",
        min=0,
        default=0,
    )  # type: ignore
    apply_decimate: BoolProperty(
        name="Apply decimate modifier",
        description="Check this to destructively decimate the geometry",
        default=False,
    )  # type: ignore
    unpack_textures: BoolProperty(
        name="Unpack Textures",
        description="Unpack the textures in a separate Textures folder. The blend file size will be lower",
        default=True,
    )  # type: ignore
    scale_model: FloatProperty(
        name="Scale",
        description="Scale the model by this amount",
        default=1,
    )  # type: ignore
    overwrite: BoolProperty(
        name="Overwrite files",
        description="Overwrite the blend file if a file with the same name exists in the folder",
        default=False,
    )  # type: ignore

    def draw(self, layout, context=None):
        layout.prop(self, "overwrite")
        layout.prop(self, "file_extension")
        layout.prop(self, "target_faces")
        layout.prop(self, "apply_decimate")
        layout.prop(self, "unpack_textures")
        layout.prop(self, "scale_model")

    def run_in_file(self, attributes=None):
        file = Path(attributes["filepath"])
        blend_name = file.parent.name if file.parent.name != "source" else file.parent.parent.name
        blend_file = str(file.parent / (blend_name + ".blend"))
        if Path(blend_file).exists() and not self.overwrite:
            print(f"{blend_file} already exists. Do not overwrite.")
        else:
            import_ops_from_file_extension[self.file_extension](filepath=str(file))
            import_and_clean(
                file,
                bpy.context,
                self.target_faces,
                self.apply_decimate,
                self.scale_model,
            )
            bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
            bpy.data.objects[0].name = blend_name
            save_file_as(
                filepath=blend_file,
                remove_backup=get_from_cache(LibraryExportSettings).remove_backup,
            )  # For unpacking we need to save the file
            if self.unpack_textures:
                bpy.ops.file.unpack_all(method="USE_LOCAL")
            save_file_as(
                filepath=blend_file,
                remove_backup=get_from_cache(LibraryExportSettings).remove_backup,
            )
        return False


class ABU_OT_ModelConvert(Operator, BatchFolderOperator):
    bl_idname = "abu.model_convert"
    bl_label = "Batch Convert Files"

    ui_library = (LibraryType.FolderExternal.value, LibraryType.UserLibrary.value, LibraryType.FileExternal.value)
    operator_settings: PointerProperty(type=ModelConvertOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=False, filter_type=False, filter_selection=False, filter_name=False)

    @property
    def file_extension(self):
        return get_from_cache(ModelConvertOperatorProperties).file_extension


def scale_my_model(obj, scale):
    # If one of the dim is > 1000 m there is a chance the model is in millimeters
    dim = max(obj.dimensions) / 1000
    i = 0
    while True:
        if dim // (10**i) == 0:
            break
        i += 1
    obj.scale = (scale / (10**i),) * 3
    with bpy.context.temp_override(selected_editable_objects=[obj]):
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def decimate_geometry_and_create_driver(obj, target_faces, apply_decimate):
    obj["target_faces"] = target_faces
    prop = obj.id_properties_ui("target_faces")
    prop.update(min=0)
    obj.property_overridable_library_set('["target_faces"]', True)

    dec_mod_name = "Decimate_collapse"
    dec_mod = obj.modifiers.new(dec_mod_name, "DECIMATE")

    driver = dec_mod.driver_add("ratio").driver
    var = driver.variables.new()
    var.name = "target"
    var.type = "SINGLE_PROP"
    target = var.targets[0]
    target.id_type = "OBJECT"
    target.id = obj
    target.data_path = '["target_faces"]'
    driver.expression = f"target / {max(1, len(obj.data.polygons))} if target > 0 else 1"

    if apply_decimate:
        with bpy.context.temp_override(object=obj):
            bpy.ops.object.modifier_apply(apply_as="DATA", modifier=dec_mod_name)


def clean_geometry(context):
    mesh_objects = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    mesh_object = mesh_objects[0]

    with context.temp_override(active_object=mesh_object, selected_editable_objects=mesh_objects):
        bpy.ops.object.join()

    with context.temp_override(mesh=mesh_object.data, selected_editable_objects=[mesh_object]):
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
        bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    mod = mesh_object.modifiers.new("weld", "WELD")
    mod.merge_threshold = 0.00001
    with context.temp_override(object=mesh_object):
        bpy.ops.object.modifier_apply(modifier="weld")

    bbox_corners = [mesh_object.matrix_world @ Vector(corner) for corner in mesh_object.bound_box]
    center = sum((Vector(b) for b in bbox_corners), Vector()) / 8
    trans = Vector((center.x, center.y, min([vec[2] for vec in bbox_corners])))
    cursor_local_loc = mesh_object.matrix_world.inverted() @ trans
    mesh_object.data.transform(Matrix.Translation(-cursor_local_loc))

    return mesh_object


def import_and_clean(
    file,
    context,
    target_faces,
    apply_decimate,
    scale_model,
):
    mesh_object = clean_geometry(context)

    decimate_geometry_and_create_driver(mesh_object, target_faces, apply_decimate)

    mesh_object.users_collection[0].objects.unlink(mesh_object)
    bpy.context.scene.collection.objects.link(mesh_object)

    scale_my_model(mesh_object, scale_model)

    bpy.data.batch_remove([o for o in bpy.data.objects if o != mesh_object])

    mesh_object.name = mesh_object.data.name = file.stem.title().replace("_", " ").replace("-", " ")

    view_3D = next(a for a in bpy.context.window.screen.areas if a.type == "VIEW_3D")
    region = next(r for r in view_3D.regions if r.type == "WINDOW")
    with bpy.context.temp_override(area=view_3D, region=region):
        bpy.ops.view3d.view_all()
