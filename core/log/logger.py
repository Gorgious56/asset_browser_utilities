class Logger:
    active = False
    _log = []
    
    @classmethod
    def log(cls, message):
        cls._log.append(message)
    
    @classmethod
    def display(cls, message):
        cls._log.append(message)
        if cls.active:
            print(message)
        