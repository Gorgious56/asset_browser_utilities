import bpy

from asset_browser_utilities.core.test.prop import TestOperator


def test_replacing_gn_tree_A_with_gn_tree_B_in_object_modifier(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=False,
    )

    test_op.op_props.tree_type = "GEOMETRY"
    test_op.op_props.node_tree_new = "NODE_TREE_GN_FROM"
    test_op.op_props.node_tree_old = "NODE_TREE_GN_TO"

    test_object = bpy.data.objects["node_tree_replace_gn"]

    assert (
        next(m for m in test_object.modifiers if m.type == "NODES").node_group.name == test_op.op_props.node_tree_old
    )

    test_op.execute()

    test_object = bpy.data.objects["node_tree_replace_gn"]
    assert (
        next(m for m in test_object.modifiers if m.type == "NODES").node_group.name == test_op.op_props.node_tree_new
    )


def test_replacing_gn_tree_A_with_gn_tree_B_in_gn_tree_C(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=False,
    )

    test_op.op_props.tree_type = "GEOMETRY"
    test_op.op_props.node_tree_new = "NODE_TREE_GN_FROM"
    test_op.op_props.node_tree_old = "NODE_TREE_GN_TO"

    test_gn = bpy.data.node_groups["NODE_TREE_GN_REPLACE_TEST"]
    assert next(n for n in test_gn.nodes if n.type == "GROUP").node_tree.name == test_op.op_props.node_tree_old

    test_op.execute()

    test_gn = bpy.data.node_groups["NODE_TREE_GN_REPLACE_TEST"]
    assert next(n for n in test_gn.nodes if n.type == "GROUP").node_tree.name == test_op.op_props.node_tree_new


def test_replacing_ng_a_with_ng_b_in_compositing(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=False,
    )

    test_op.op_props.tree_type = "COMPOSITING"
    test_op.op_props.node_tree_new = "NODE_TREE_COMP_FROM"
    test_op.op_props.node_tree_old = "NODE_TREE_COMP_TO"

    comp = bpy.context.scene.node_tree
    assert next(n for n in comp.nodes if n.type == "GROUP").node_tree.name == test_op.op_props.node_tree_old

    test_op.execute()

    comp = bpy.context.scene.node_tree
    assert next(n for n in comp.nodes if n.type == "GROUP").node_tree.name == test_op.op_props.node_tree_new


def test_replacing_ng_a_with_ng_b_in_shader(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=False,
    )

    test_op.op_props.tree_type = "SHADER"
    test_op.op_props.node_tree_new = "NODE_TREE_SHADER_FROM"
    test_op.op_props.node_tree_old = "NODE_TREE_SHADER_TO"

    mat = bpy.data.materials["NODE_TREE_REPLACE_MATERIAL"]
    assert next(n for n in mat.node_tree.nodes if n.type == "GROUP").node_tree.name == test_op.op_props.node_tree_old

    test_op.execute()

    mat = bpy.data.materials["NODE_TREE_REPLACE_MATERIAL"]
    assert next(n for n in mat.node_tree.nodes if n.type == "GROUP").node_tree.name == test_op.op_props.node_tree_new
