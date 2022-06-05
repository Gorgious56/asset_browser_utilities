from asset_browser_utilities.core.preferences.tool import get_preferences


class Logger:
    _log = []
    
    @classmethod
    def log(cls, message):
        cls._log.append(message)
    
    @classmethod
    def display(cls, message):
        cls._log.append(message)
        if get_preferences().verbose:
            print(message)
        