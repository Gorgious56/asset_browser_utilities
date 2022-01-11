import bpy


def item_exists(name, _type):
    library = getattr(bpy.data, _type.lower() + "s")
    return library.get(name) is not None
