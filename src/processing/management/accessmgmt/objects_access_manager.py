class MultiAccessManager:

    __instance = None
    multi_access_objects = {}

    def __new__(cls):

        if cls.__instance is None:
            cls.__instance = super(MultiAccessManager, cls).__new__(cls)

        return cls.__instance
