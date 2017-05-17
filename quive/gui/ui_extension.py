ext_classes = set()
deferred_definition = dict()


def ui_extension(cls):
    ext_classes.add(cls)
    return cls


def deferred_define(func):
    deferred_definition[func.__name__] = func
    return func


def run_deferred_function(name, *args, **kwargs):
    return deferred_definition[name](*args, **kwargs)
