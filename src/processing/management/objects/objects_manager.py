from processing.management.logger.logger_threads_manager import LoggerThreadManager


class ObjectsManager:

    __instance = None
    __objects = {}
    __logger = LoggerThreadManager()

    def __new__(cls):

        if cls.__instance is None:
            cls.__instance = super(ObjectsManager, cls).__new__(cls)

        return cls.__instance

    @classmethod
    def __getitem__(cls, object_name):

        _object = None
        repr_object_name = None

        try:
            repr_object_name = repr(object_name)
            _object = cls.__objects[object_name]

        except KeyError:
            cls.__logger.exception(f"{repr_object_name} doesn't exist!")
            return None

        except AttributeError as E:
            cls.__logger.exception(f"_object is not a class! - {E}")
            return None

        else:
            cls.__logger.debug(f"Found {repr_object_name}")
            return _object

    @classmethod
    def create_object(cls, _object, *args, **kwargs):

        repr_object_name = None

        try:
            object_name = _object.__name__
            repr_object_name = repr(object_name)
            cls.__objects[object_name] = _object(*args, **kwargs)

        except AttributeError:
            cls.__logger.exception("'_object' is not a class!")
            return None

        except Exception:
            cls.__logger.exception(f"Some Error occurred while creating object {repr_object_name}!")
            return None

        else:
            cls.__logger.debug(f"Successfully created Object {repr_object_name}!")
            return cls.__objects[object_name]

    @classmethod
    def delete_object(cls, object_name):

        repr_object_name = repr(object_name)

        try:
            del cls.__objects[object_name]

        except KeyError:
            cls.__logger.exception(f"{repr_object_name} doesn't exist!")

        else:
            cls.__logger.debug(f"Successfully deleted {repr_object_name}")
