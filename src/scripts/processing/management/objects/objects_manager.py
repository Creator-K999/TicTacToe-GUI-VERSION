from sys import exit as _exit
from inspect import stack

from logger.logger import Log


class ObjectsManager:

    __objects = {}

    def __init__(self):
        raise NotImplementedError("Cannot Instantiate ObjectsManager!")

    @classmethod
    def get_object_by_name(cls, object_name):

        current_stack = stack()[1]

        if not isinstance(object_name, str):
            Log.error(f"String required, got {type(object_name)} instead!", current_stack)
            cls.destruct_objects()
            _exit(-1)

        Log.info(f"Trying to get {object_name} instance...", current_stack)

        try:
            _object = cls.__objects[object_name]

        except AttributeError as E:
            Log.error(f"Error: {E}", current_stack)

        except KeyError:
            Log.exception(f"'{object_name}' doesn't exist!", current_stack)

        except Exception as E:
            Log.error(f"Error: {E}")

        else:
            Log.debug(f"Found '{object_name}'", current_stack)
            return _object

    @classmethod
    def destruct_objects(cls):
        current_stack = stack()[1]
        leaks_found = len(cls.__objects) != 0

        Log.debug("Looking for memory leaks!", current_stack)
        for _object in (*cls.__objects,):
            Log.warning(f"Found a memory leak!, object is {_object}", current_stack)
            del cls.__objects[_object]

        if leaks_found:
            Log.warning("Found some leaks but cleaned them up!", current_stack)

        else:
            Log.info("No leaks found!", current_stack)

    @classmethod
    def create_object(cls, _object, *args, custom_name=None, **kwargs):
        current_stack = stack()[1]

        if not isinstance(_object, type):
            Log.error(f"This Static Method Only Supports Classes, got {type(_object)} instead!", current_stack)
            cls.destruct_objects()
            _exit(-1)

        object_name = custom_name or _object.__name__

        if object_name in cls.__objects:
            Log.error(f"{object_name} already exist, please use a custom name for it!")
            cls.destruct_objects()
            _exit(-1)

        try:
            cls.__objects[object_name] = _object(*args, **kwargs)

        except Exception as E:
            Log.error(f"Error occurred while instantiating object!\n\tError: {E}", current_stack)

        else:
            Log.debug(f"Successfully created Object '{object_name}'!", current_stack)
            return cls.__objects[object_name]

    @classmethod
    def delete_object(cls, object_name):
        current_stack = stack()[1]

        try:
            del cls.__objects[object_name]

        except KeyError:
            Log.error(f"'{object_name}' doesn't exist!", current_stack)

        except Exception as E:
            Log.error(f"Error: {E}", current_stack)

        else:
            Log.debug(f"Successfully deleted '{object_name}'", current_stack)
