from abc import ABCMeta


class SingletonRegistryMeta(ABCMeta):
    """A generic metaclass for singleton + automatic registry behavior."""

    _registries: dict[type, dict[str, object]] = {}

    def __call__(cls, *args, **kwargs):
        """
        Ensure singleton behavior per class.
        Creates a registry for this class type if it doesn't exist.
        """
        registry = cls._registries.setdefault(cls, {})

        # Check for existing instance in registry by name (if the name is set)
        if getattr(cls, "name", None) in registry:
            return registry[cls.name]

        # Create a new instance using the parent class's `__call__`
        instance = super().__call__(*args, **kwargs)

        # Register the instance if it has a 'name' attribute
        if hasattr(instance, "name"):
            registry[instance.name] = instance

        # Check if the class has a parent (for subclassing support)
        cls._register_in_parents(instance)

        return instance

    def _register_in_parents(cls, instance):
        """Register the instance in parent class registries, up to the first class
        with the SingletonRegistryMeta metaclass."""
        # Check if the class has a parent (for subclassing support)
        parent_class = cls.__base__

        # Stop if the parent class is the base class of SingletonRegistryMeta
        if parent_class is not object and isinstance(
            parent_class, SingletonRegistryMeta
        ):
            parent_registry = parent_class._registries.setdefault(parent_class, {})

            # Only register in the parent registry if it's not already registered
            if getattr(instance, "name", None) and instance.name not in parent_registry:
                parent_registry[instance.name] = instance

            # Recursively register in the parent's parent (up the hierarchy) if
            # necessary
            parent_class._register_in_parents(instance)

    def get_by_name(cls, name: str) -> object:
        """Return the singleton instance of this class type by name."""
        registry = cls._registries.get(cls, {})
        if name not in registry:
            raise ValueError(f"Unknown {cls.__name__} '{name}'")
        return registry[name]

    @property
    def registry(cls):
        """Return all registered instances of this class type."""
        return dict(cls._registries.get(cls, {}))
