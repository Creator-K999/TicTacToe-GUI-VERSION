from scripts.processing.management.logger.logger_threads_manager import LoggerThreadManager


PLAYERS_INFO = {}


def connect_object(_object, method_to_connect):
    if _object is None:
        LoggerThreadManager.warning(f"Couldn't Find '{_object.__name__}'!")

    else:
        object_name = _object.__name__
        method_to_connect_name = method_to_connect.__name__
        LoggerThreadManager.info(f"Found '{object_name}'")

        LoggerThreadManager.debug(f"Connecting '{object_name}' with '{method_to_connect_name}'")
        try:
            _object.clicked.connect(method_to_connect)

        except AttributeError:
            LoggerThreadManager.exception(f"Couldn't connect '{object_name}' with "
                                          f"'{method_to_connect_name}'")

        except Exception:
            LoggerThreadManager.exception(f"Something went wrong "
                                          f"while connecting {object_name} with {method_to_connect_name}")

        else:
            LoggerThreadManager.info(f"Successfully connected '{object_name}' with "
                                     f"'{method_to_connect_name}'")
