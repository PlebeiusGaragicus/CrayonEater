class Singleton:
    _instance = None
    def __init__(self):
        raise Exception("Cannot directly instantiate a Singleton. Access via get_instance()")
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance
