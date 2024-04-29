from importlib.util import module_from_spec, spec_from_file_location
from inspect import getmembers, isclass
from types import ModuleType


def import_file(filepath: str, module_name: str):
    spec = spec_from_file_location(module_name, filepath)
    assert spec
    module = module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def default(cls):
    setattr(cls, "DEFAULT", True)
    return cls


def get_default_class(module: ModuleType) -> type | None:
    for _, cls in getmembers(module):
        if isclass(cls):
            if getattr(cls, "DEFAULT", None):
                return cls
    return None
