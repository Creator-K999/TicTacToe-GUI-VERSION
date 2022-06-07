from processing.management.logger.logger_threads_manager import LoggerThreadManager


class ObjectsManager:

    __objects = {}

    @classmethod
    def get_object_by_name(cls, object_name):

        LoggerThreadManager.info(f"Trying to get {object_name} instance...")

        _object = None
        repr_object_name = None

        try:
            repr_object_name = repr(object_name)
            _object = cls.__objects[object_name]

        except KeyError:
            LoggerThreadManager.exception(f"{repr_object_name} doesn't exist!")
            return None

        except AttributeError as E:
            LoggerThreadManager.exception(f"_object is not a class! - {E}")
            return None

        else:
            LoggerThreadManager.debug(f"Found {repr_object_name}")
            return _object

    @classmethod
    def destruct_objects(cls):
        leak_found = False
        LoggerThreadManager.debug("Looking for memory leaks!")
        for _object in [*cls.__objects]:
            leak_found = True
            LoggerThreadManager.warning(f"Found a memory leak!, object is {_object}")
            del cls.__objects[_object]

        if leak_found:
            LoggerThreadManager.warning("Found some leaks but cleaned them up!")

    @classmethod
    def create_object(cls, _object, *args, singleton=True, **kwargs):

        try:
            object_name = _object.__name__
            repr_object_name = f"'{object_name}'"

        except AttributeError:
            LoggerThreadManager.exception(f"object '{_object}' is not a class!")
            return None

        else:

            if singleton:
                LoggerThreadManager.debug(f"Looking for an instance of {repr_object_name}")

                if object_name in cls.__objects:
                    LoggerThreadManager.info(f"Found an instance of {object_name}")
                    return cls.__objects[object_name]

                else:
                    LoggerThreadManager.info(f"Couldn't find an instance of {object_name}, Trying to create one...")

        try:
            cls.__objects[object_name] = _object(*args, **kwargs)

        except Exception:
            LoggerThreadManager.exception(f"Some Error occurred while creating object {repr_object_name}!")
            return None

        else:
            LoggerThreadManager.debug(f"Successfully created Object {repr_object_name}!")
            return cls.__objects[object_name]

    @classmethod
    def delete_object(cls, object_name):

        LoggerThreadManager.info(f"Trying to delete {object_name} instance...!")
        repr_object_name = repr(object_name)

        try:
            del cls.__objects[object_name]

        except KeyError:
            LoggerThreadManager.exception(f"{repr_object_name} doesn't exist!")

        except Exception:
            LoggerThreadManager.exception("Error happened!")

        else:
            LoggerThreadManager.debug(f"Successfully deleted {repr_object_name}")
