from processing.management.logger.logger import Log


class ObjectsManager:

    __objects = {}

    @classmethod
    def get_object_by_name(cls, object_name):

        Log.info(f"Trying to get {object_name} instance...")

        repr_object_name = None

        try:
            repr_object_name = repr(object_name)
            _object = cls.__objects[object_name]

        except KeyError:
            Log.exception(f"{repr_object_name} doesn't exist!")

        except AttributeError as E:
            Log.exception(f"_object is not a class! - {E}")

        except Exception as E:
            Log.error(f"ERROR: {E}")

        else:
            Log.debug(f"Found {repr_object_name}")
            return _object

    @classmethod
    def destruct_objects(cls):
        leak_found = len(cls.__objects) != 0

        Log.debug("Looking for memory leaks!")
        for _object in (*cls.__objects,):
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

            if object_name in cls.__objects:
                raise ValueError("Object Already Exist!")

            cls.__objects[object_name] = _object(*args, **kwargs)

        except AttributeError as E:
            Log.exception(f"ERROR: {E}")

        except ValueError as E:
            Log.error(f"ERROR: {E}")

        except Exception as E:
            Log.exception(f"Some Error occurred while creating object {repr_object_name}!\n\tERROR: {E}")

        else:
            Log.debug(f"Successfully created Object {repr_object_name}!")
            return cls.__objects[object_name]

    @classmethod
    def delete_object(cls, object_name):

        Log.info(f"Trying to delete {object_name} object...!")
        repr_object_name = f"'{object_name}'"

        try:
            del cls.__objects[object_name]
            Log.debug(f"Successfully deleted {repr_object_name}")

        except KeyError:
            Log.exception(f"{repr_object_name} doesn't exist!")

        except Exception as E:
            Log.exception(f"Error happened!{E}")
