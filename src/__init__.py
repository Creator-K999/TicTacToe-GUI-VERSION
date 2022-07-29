from inspect import stack

from processing.management.logger.logger import Log

last_login_info = {}


def connect_object(_object, method_to_connect, *, custom_connect="clicked"):
    current_stack = stack()[1]

    if _object is None:
        Log.warning(f"Couldn't Find '{_object.__name__}'!", current_stack)

    else:
        object_name = _object.objectName()
        method_to_connect_name = method_to_connect.__name__
        Log.info(f"Found '{object_name}'", current_stack)

        Log.debug(f"Connecting '{object_name}' with '{method_to_connect_name}'", current_stack)
        try:
            getattr(_object, custom_connect).connect(method_to_connect)

        except AttributeError as E:
            Log.error(f"Couldn't connect '{object_name}' with "
                      f"'{method_to_connect_name}'\nERROR: {E}", current_stack)

        except Exception as E:
            Log.exception(f"Something went wrong "
                          f"while connecting {object_name} with {method_to_connect_name}! {E}", current_stack)

        else:
            Log.info(f"Successfully connected '{object_name}' with "
                     f"'{method_to_connect_name}'", current_stack)
