def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as error:
            return str(error)
        except Exception:
            print("Unexpected error occurred:")
            print(traceback.format_exc())
            return "Internal error. Please try again."
    return inner
