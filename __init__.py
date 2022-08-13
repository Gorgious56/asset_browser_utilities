# This whole addon is released under CC0 licence. Do with it what you wish.
# Backup your files. No result guaranteed whatsoever.


bl_info = {
    "name": "Asset Browser Utilities ",
    "author": "Gorgious",
    "description": "Asset Browser QOL tools and batch operations",
    "blender": (3, 0, 0),
    "version": (0, 2, 4),
    "location": "",
    "warning": "",
    "category": "Import-Export",
    "doc_url": "https://github.com/Gorgious56/asset_browser_utilities/blob/master/README.md",
}


from . import auto_load


def register():
    auto_load.init()
    auto_load.register()


def unregister():
    auto_load.unregister()


if __name__ == "__main__":
    register()
