from __future__ import annotations

from typing import Dict, Generic, Type, TypeVar, cast

# Define a generic type variable for subclasses of BaseElement
T = TypeVar("T", bound="Registry")


class Registry(Generic[T]):
    """
    Creates a registry of all subclasses when inherited.

    This class is designed to be inherited by other classes. When inherited,
    it creates a class attribute '_registry' which records all subclasses of
    the class. The subclasses get recorded as soon as they are imported. They
    therefore do not need to be initialized to appear in the registry. Each
    subclass must have a class attribute "name" which exists before initialization.
    """

    # The registry will be a dictionary of class names (strings) to class types
    _registry: Dict[str, Type[T]] = {}

    def __init_subclass__(cls, is_base_registry: bool = False, **kwargs):
        """Initialize subclass and register it in its own registry."""
        super().__init_subclass__(**kwargs)

        # Recreate registry to ensure that there is no cross-contamination between
        # different class that inherit the Registry class
        # if "_registry" not in cls.__dict__:
        #     cls._registry = {}

        # Initialize registry if class is intended as base registry
        if is_base_registry:
            cls._registry = {}

        # Ensure the subclass defines 'name' attribute
        if not hasattr(cls, "name"):
            raise AttributeError(
                f"Subclass {cls.__name__} should define a class variable 'name'."
            )

        # Check if the name is already used by a different class type
        if cls.name in cls._registry and type(cls._registry[cls.name]) is not type(cls):
            raise ValueError(
                f"Two classes of type {type(cls)} cannot have the same name."
                f"Class with name '{cls.name}' exists for both {type(cls)} and "
                f"{type(cls._registry[cls.name])}."
            )

        cls._registry[cls.name] = cast(Type[T], cls)

    @classmethod
    def get_registry(cls) -> Dict[str, Type[T]]:
        """Return the registry for the class."""
        return cls._registry

    @classmethod
    def get_by_name(cls, name: str) -> Type[T] | None:
        """Get subclass from by name."""
        if name in cls._registry.keys():
            return cls._registry[name]
        else:
            return None

    @classmethod
    def clear_registry(cls):
        cls._registry.clear()

    @classmethod
    def update_registry(cls, new_registry: Dict[str, Type[T]]):
        cls._registry.update(new_registry)
