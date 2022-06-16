from processing.management.logger.logger import Log


class ObjectsManager:

    __objects = {}

    def __init__(self):
        raise NotImplementedError("Cannot Instantiate ObjectsManager!")

    @classmethod
    def get_object_by_name(cls, object_name):

        Log.info(f"Trying to get {object_name} instance...")

        _object = None
        repr_object_name = None

        try:
            repr_object_name = repr(object_name)
            _object = cls.__objects[object_name]

        except KeyError:
            Log.exception(f"{repr_object_name} doesn't exist!")
            return None

        except AttributeError as E:
            Log.exception(f"_object is not a class! - {E}")
            return None

        else:
            Log.debug(f"Found {repr_object_name}")
            return _object

    @classmethod
    def destruct_objects(cls):
        leak_found = False
        Log.debug("Looking for memory leaks!")
        for _object in [*cls.__objects]:
            leak_found = True
            Log.warning(f"Found a memory leak!, object is {_object}")
            del cls.__objects[_object]

        if leak_found:
            Log.warning("Found some leaks but cleaned them up!")

        else:
            Log.info("No leaks found!")

    @classmethod
    def create_object(cls, _object, *args, custom_name=None, **kwargs):

        repr_object_name = None

        try:
            object_name = custom_name if custom_name else _object.__name__
            repr_object_name = f"'{object_name}'"
            cls.__objects[object_name] = _object(*args, **kwargs)

        except AttributeError:
            Log.exception(f"object '{_object}' is not a class!")
            return None

        except Exception as E:
            Log.exception(f"Some Error occurred while creating object {repr_object_name}!{E}")
            return None

        Log.debug(f"Successfully created Object {repr_object_name}!")
        return cls.__objects[object_name]

    @classmethod
    def delete_object(cls, object_name):

        Log.info(f"Trying to delete {object_name} instance...!")
        repr_object_name = repr(object_name)

        try:
            del cls.__objects[object_name]

        except KeyError:
            Log.exception(f"{repr_object_name} doesn't exist!")

        except Exception as E:
            Log.exception(f"Error happened!{E}")

        else:
            Log.debug(f"Successfully deleted {repr_object_name}")
