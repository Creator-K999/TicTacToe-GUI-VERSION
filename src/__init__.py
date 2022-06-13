from processing.management.logger.logger import Log


def connect_object(_object, method_to_connect):
    if _object is None:
        Log.warning(f"Couldn't Find '{_object.__name__}'!")

    else:
        object_name = _object.objectName()
        method_to_connect_name = method_to_connect.__name__
        Log.info(f"Found '{object_name}'")

        Log.debug(f"Connecting '{object_name}' with '{method_to_connect_name}'")
        try:
            _object.clicked.connect(method_to_connect)

        except AttributeError:
            Log.exception(f"Couldn't connect '{object_name}' with "
                          f"'{method_to_connect_name}'")

        except Exception as E:
            Log.exception(f"Something went wrong "
                          f"while connecting {object_name} with {method_to_connect_name}! {E}")

        else:
            Log.info(f"Successfully connected '{object_name}' with "
                     f"'{method_to_connect_name}'")
