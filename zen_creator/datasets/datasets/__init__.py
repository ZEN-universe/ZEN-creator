import pkgutil
import importlib
import inspect
from pathlib import Path

__all__ = []

# for _, module_name, _ in pkgutil.iter_modules([str(Path(__file__).parent)]):
#     module = importlib.import_module(f".{module_name}", package=__name__)
    
#     for name, obj in inspect.getmembers(module, inspect.isclass):
        
#         if obj.__module__ == module.__name__:
#             globals()[name] = obj
#             __all__.append(name)