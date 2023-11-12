from asset_browser_utilities.core.console.parser import ArgumentsParser


class CommandLineExecuteBase:
    def __init__(self) -> None:
        parser = ArgumentsParser()
        self.attributes = {
            attr_name: attr_type(parser.get_arg_value(attr_name))
            for attr_name, attr_type in self.__class__.__annotations__.items()
        }
