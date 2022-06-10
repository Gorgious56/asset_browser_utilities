from asset_browser_utilities.core.cache.tool import get_cache, get_from_cache
from asset_browser_utilities.core.operator.prop import CurrentOperatorProperty


def setup_current_operator(attr_name):
    prop = getattr(get_cache(), attr_name)
    get_from_cache(CurrentOperatorProperty).class_name = str(prop.__class__)


def execute_logic(logic_class):
    logic = logic_class()
    logic.save_file = lambda: None
    logic.execute_next_blend()
