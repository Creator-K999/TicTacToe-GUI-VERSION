from processing.management.logger.logger_threads_manager import LoggerThreadManager


class ObjectsManager:

    __objects = {}
    __logger = LoggerThreadManager()

    @classmethod
    def get_object_by_name(cls, object_name):

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
    def destruct_objects(cls):
        cls.__logger.debug("Cleaning Objects!")

        for _object in cls.__objects:
            cls.__logger.warning(f"Found a memory leak!, object is {_object}")
            cls.delete_object(_object)

        cls.__logger.info("Objects leaked has been deleted!")

    @classmethod
    def create_object(cls, _object, *args, **kwargs):

        repr_object_name = None

        try:
            object_name = _object.__name__

            repr_object_name = f"'{object_name}'"
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
            try:
                cls.__logger.debug(f"Trying to call the destructor manually on {repr_object_name}!")
                cls.__objects[object_name].__del__()

            except Exception:
                cls.__logger.exception(f"Error! could not call the destructor manually on {repr_object_name}!")

            del cls.__objects[object_name]

        except KeyError:
            cls.__logger.exception(f"{repr_object_name} doesn't exist!")

        except Exception:
            cls.__logger.exception("Error happend!")

        else:
            cls.__logger.debug(f"Successfully deleted {repr_object_name}")
