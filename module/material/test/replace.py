import bpy

from asset_browser_utilities.core.test.prop import TestOperator

from asset_browser_utilities.module.material.operator.replace import MaterialReplaceBatchExecute


def test_replacing_material_a_with_material_b_on_assets(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=True,
        op_name="op_material_replace",
        logic_class=MaterialReplaceBatchExecute,
    )

    test_op.op_props.material_from = "MATERIAL_REPLACE_FROM"
    test_op.op_props.material_to = "MATERIAL_REPLACE_TO"

    test_object_asset = bpy.data.objects["material_replace_asset"]
    test_object_not_asset = bpy.data.objects["material_replace_not_asset"]

    for obj in (test_object_asset, test_object_not_asset):
        assert test_op.op_props.material_from in [m_s.material.name for m_s in obj.material_slots]
        assert test_op.op_props.material_to in [m_s.material.name for m_s in obj.material_slots]

    test_op.execute()

    test_object_asset = bpy.data.objects["material_replace_asset"]
    test_object_not_asset = bpy.data.objects["material_replace_not_asset"]

    assert test_op.op_props.material_from in [m_s.material.name for m_s in test_object_asset.material_slots]
    assert test_op.op_props.material_to not in [m_s.material.name for m_s in test_object_asset.material_slots]
    assert test_op.op_props.material_from in [m_s.material.name for m_s in test_object_not_asset.material_slots]
    assert test_op.op_props.material_to in [m_s.material.name for m_s in test_object_not_asset.material_slots]


def test_replacing_material_a_with_material_b_on_all_objects(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=False,
        op_name="op_material_replace",
        logic_class=MaterialReplaceBatchExecute,
    )

    test_op.op_props.material_from = "MATERIAL_REPLACE_FROM"
    test_op.op_props.material_to = "MATERIAL_REPLACE_TO"

    test_object_asset = bpy.data.objects["material_replace_asset"]
    test_object_not_asset = bpy.data.objects["material_replace_not_asset"]

    for obj in (test_object_asset, test_object_not_asset):
        assert test_op.op_props.material_from in [m_s.material.name for m_s in obj.material_slots]
        assert test_op.op_props.material_to in [m_s.material.name for m_s in obj.material_slots]

    test_op.execute()

    test_object_asset = bpy.data.objects["material_replace_asset"]
    test_object_not_asset = bpy.data.objects["material_replace_not_asset"]

    for obj in (test_object_asset, test_object_not_asset):
        assert test_op.op_props.material_from in [m_s.material.name for m_s in obj.material_slots]
        assert test_op.op_props.material_to not in [m_s.material.name for m_s in obj.material_slots]
