import os
from pathlib import Path
import bpy
from mathutils import Matrix, Vector
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty
from bpy.types import Operator

from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.operator.tool import BatchFolderOperator
from asset_browser_utilities.core.cache.tool import get_from_cache


import_ops_from_file_extension = {
    "gltf": bpy.ops.import_scene.gltf,
    "fbx": bpy.ops.import_scene.fbx,
    "stl": bpy.ops.wm.stl_import,
    "obj": bpy.ops.wm.obj_import,
}


class ModelConvertOperatorProperties(PropertyGroup, BaseOperatorProps):
    file_extension: bpy.props.EnumProperty(
        items=(
            ("gltf",) * 3,
            ("fbx",) * 3,
            ("stl",) * 3,
            ("obj",) * 3,
        ),
        name="File Type",
    )

    def draw(self, layout, context=None):
        layout.prop(self, "file_extension")

    def run_in_file(self, attributes=None):
        import_ops_from_file_extension[self.file_extension](filepath=str(self.file))
        self.save_file(filepath=str(self.file.parent / (self.file.parent.name + ".blend")))
        self.execute_next_file()


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


def unselect_all(context):
    bpy.ops.object.select_all(action="DESELECT")
    context.view_layer.objects.active = None


def select_and_set_active(obj, context):
    unselect_all(context)
    obj.select_set(True)
    context.view_layer.objects.active = obj


def scale_my_model(obj, scale, expected_dimension, context):
    # If one of the dim is > 1000 m there is a chance the model is in millimeters
    dim = max(obj.dimensions) / 1000
    i = 0
    while True:
        if dim // (10 ** i) == 0:
            break
        i += 1
    obj.scale = (scale / (10 ** i),) * 3
    bpy.ops.object.transform_apply({"selected_editable_objects": [obj]}, location=True, rotation=True, scale=True)


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

    window = context.window_manager.windows[0]
    screen = window.screen

    bpy.ops.object.join({"active_object": mesh_object, "selected_editable_objects": mesh_objects})

    with bpy.context.temp_override(mesh=mesh_object.data, selected_editable_objects=[mesh_object]):
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
        bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    mesh_object.modifiers.new("weld", "WELD")
    with bpy.context.temp_override(object=mesh_object):
        bpy.ops.object.modifier_apply(modifier="weld")

    bbox_corners = [mesh_object.matrix_world @ Vector(corner) for corner in mesh_object.bound_box]
    center = sum((Vector(b) for b in bbox_corners), Vector()) / 8
    trans = Vector((center.x, center.y, min([vec[2] for vec in bbox_corners])))
    cursor_local_loc = mesh_object.matrix_world.inverted() @ trans
    mesh_object.data.transform(Matrix.Translation(-cursor_local_loc))

    return mesh_object


class BatchConvertGLTF(Operator, BatchFolderOperator):
    bl_idname = "abu.model_convertd"
    bl_label = "Batch Convert GLTF Files"

    filter_glob: StringProperty(
        default="",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    write_in_subfolders: BoolProperty(
        name="Save in subfolders",
        description="If Checked, blend files will be saved in the source sub folders\nOtherwise they are saved in the root folder",
        default=True,
    )
    overwrite: BoolProperty(
        name="Overwrite files",
        description="Overwrite the blend file if a file with the same name exists in the folder",
        default=True,
    )
    prevent_backup: BoolProperty(
        name="Remove Backup",
        description="Check to automatically delete the creation of backup files when 'Save Versions' is enabled in the preferences\nThis will prevent duplicating files when they are overwritten\nWarning : Backup files will be deleted permantently",
        default=False,
    )
    target_faces: IntProperty(
        name="Target Faces",
        description="The decimate modifier will give this number of polygons (0 keeps the same number of faces)",
        min=0,
        default=0,
    )
    apply_decimate: BoolProperty(
        name="Apply decimate modifier",
        description="Check this to destructively decimate the geometry",
        default=False,
    )
    unpack_textures: BoolProperty(
        name="Unpack Textures",
        description="Unpack the textures in a separate Textures folder. The blend file size will be lower",
        default=False,
    )
    scale_model: FloatProperty(
        name="Scale",
        description="Scale the model by this amount",
        default=1,
    )
    expected_dimension: IntProperty(
        name="Expected maximum dimension",
        description="Scale the model by this amount",
        default=1,
        min=1,
    )
    file_type: EnumProperty(items=(("gltf",) * 3, ("fbx",) * 3), name="File Type")

    def execute(self, context):
        folder = Path(self.filepath).parent
        files = [fp for fp in folder.glob(f"**/*.{self.file_type}") if fp.is_file()]
        for i, file in enumerate(files):
            if i == 0:
                wipe_and_purge_blend()

            print(f"{len(files) - i} files left")
            blend_file = file.with_suffix(".blend")
            if blend_file.exists() and not self.overwrite:
                print(f"{blend_file} already exists. Do not overwrite.")
                continue

            bpy.ops.wm.save_as_mainfile(
                filepath=str(blend_file)
            )  # FIXME find a way to specify filepath for unpacking without saving ? Otherwise when unpacking ressources are saved at i-1 file location

            import_and_clean(
                file,
                context,
                self.target_faces,
                self.apply_decimate,
                self.scale_model,
                self.expected_dimension,
                self.file_type,
            )
            if self.unpack_textures:
                bpy.ops.file.unpack_all(method="USE_LOCAL")
            bpy.ops.wm.save_as_mainfile(filepath=str(blend_file))
            if self.prevent_backup:
                backup = str(blend_file) + "1"
                if os.path.exists(backup):
                    print("Removing backup " + backup)
                    os.remove(backup)
            wipe_and_purge_blend()

        print("Batch conversion completed")
        return {"FINISHED"}


def wipe_and_purge_blend():
    bpy.data.batch_remove(bpy.data.objects)
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)


def import_and_clean(file, context, target_faces, apply_decimate, scale_model, expected_dimension, file_type):
    if file_type == "gltf":
        bpy.ops.import_scene.gltf(filepath=str(file))
    elif file_type == "fbx":
        bpy.ops.import_scene.fbx(filepath=str(file))

    mesh_object = clean_geometry(context)

    decimate_geometry_and_create_driver(mesh_object, target_faces, apply_decimate)

    mesh_object.users_collection[0].objects.unlink(mesh_object)
    bpy.data.collections[0].objects.link(mesh_object)

    scale_my_model(mesh_object, scale_model, expected_dimension, context)

    bpy.data.batch_remove([o for o in bpy.data.objects if o != mesh_object])

    mesh_object.name = mesh_object.data.name = file.stem.title().replace("_", " ").replace("-", " ")

    view_3D = next(a for a in bpy.context.window.screen.areas if a.type == "VIEW_3D")
    region = next(r for r in view_3D.regions if r.type == "WINDOW")
    bpy.ops.view3d.view_all({"area": view_3D, "region": region})


def menu_func_import(self, context):
    self.layout.operator(BatchConvertGLTF.bl_idname, text="Batch Convert GLTF Files")


def register():
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
