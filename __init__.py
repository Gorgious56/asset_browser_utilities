# This whole addon is released under CC0 licence. Do with it what you wish.
# Backup your files. No result guaranteed whatsoever.


bl_info = {
    "name": "Asset Browser Utilities ",
    "author": "Gorgious",
    "description": "Asset Browser QOL tools and batch operations",
    "blender": (4, 0, 0),
    "version": (0, 3, 0),
    "location": "",
    "warning": "",
    "category": "Import-Export",
    "doc_url": "https://github.com/Gorgious56/asset_browser_utilities/blob/master/README.md",
}


from . import auto_load
from asset_browser_utilities.core.cache.prop import Cache


def register():
    auto_load.init()
    auto_load.register()
    Cache.init()


def unregister():
    auto_load.unregister()


if __name__ == "__main__":
    register()
