import bpy

from asset_browser_utilities.core.test.prop import TestOperator


def test_replacing_material_a_with_material_b_on_assets(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=True,
    )

    test_op.op_props.material_to_override = "MATERIAL_REPLACE_FROM"
    test_op.op_props.material_to_keep = "MATERIAL_REPLACE_TO"

    test_object_asset = bpy.data.objects["material_replace_asset"]
    test_object_not_asset = bpy.data.objects["material_replace_not_asset"]

    for obj in (test_object_asset, test_object_not_asset):
        assert test_op.op_props.material_to_override in [m_s.material.name for m_s in obj.material_slots]
        assert test_op.op_props.material_to_keep in [m_s.material.name for m_s in obj.material_slots]

    test_op.execute()

    test_object_asset = bpy.data.objects["material_replace_asset"]
    test_object_not_asset = bpy.data.objects["material_replace_not_asset"]

    assert test_op.op_props.material_to_override not in [m_s.material.name for m_s in test_object_asset.material_slots]
    assert test_op.op_props.material_to_keep in [m_s.material.name for m_s in test_object_asset.material_slots]
    assert test_op.op_props.material_to_override not in [m_s.material.name for m_s in test_object_not_asset.material_slots]
    assert test_op.op_props.material_to_keep in [m_s.material.name for m_s in test_object_not_asset.material_slots]


def test_replacing_material_a_with_material_b_on_all_objects(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=False,
    )

    test_op.op_props.material_to_override = "MATERIAL_REPLACE_FROM"
    test_op.op_props.material_to_keep = "MATERIAL_REPLACE_TO"

    test_object_asset = bpy.data.objects["material_replace_asset"]
    test_object_not_asset = bpy.data.objects["material_replace_not_asset"]

    for obj in (test_object_asset, test_object_not_asset):
        assert test_op.op_props.material_to_override in [m_s.material.name for m_s in obj.material_slots]
        assert test_op.op_props.material_to_keep in [m_s.material.name for m_s in obj.material_slots]

    test_op.execute()

    test_object_asset = bpy.data.objects["material_replace_asset"]
    test_object_not_asset = bpy.data.objects["material_replace_not_asset"]

    for obj in (test_object_asset, test_object_not_asset):
        assert test_op.op_props.material_to_keep in [m_s.material.name for m_s in obj.material_slots]
        assert test_op.op_props.material_to_override not in [m_s.material.name for m_s in obj.material_slots]
