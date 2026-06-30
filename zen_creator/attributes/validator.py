from zen_creator.attributes.constants import ATTRIBUTES_SUPPORTING_LISTS
from zen_creator.attributes.types import DataFrame


class AttributeValidator:
    """Class for validating attribute values.

    Attributes:
        minimum_value (float | None):
            Minimum allowed value for the attribute (inclusive).
        maximum_value (float | None):
            Maximum allowed value for the attribute (inclusive).
    """

    minimum_value: float | None = None
    maximum_value: float | None = None

    # ---------- Validation Helpers ----------

    def validate_list_default_value(self, name: str, value: list) -> None:
        """Validate that a list default value is allowed for this attribute.

        Args:
            name: The name of the attribute being validated.
            value: The list value to validate.

        Raises:
            ValueError: If the attribute doesn't support lists or has invalid structure.
        """
        if name not in ATTRIBUTES_SUPPORTING_LISTS:
            raise ValueError(
                f"Attribute '{name}' does not support a list as default value. "
                f"Only {', '.join(sorted(ATTRIBUTES_SUPPORTING_LISTS))} support "
                "lists."
            )

        if name == "conversion_factor":
            for i, entry in enumerate(value):
                if not isinstance(entry, dict):
                    raise ValueError(
                        f"Entry {i} in conversion_factor list must be a dict, "
                        f"got {type(entry).__name__}."
                    )
                for name, factor in entry.items():
                    if "default_value" not in factor or "unit" not in factor:
                        raise ValueError(
                            f"Entry {name} in conversion_factor list must contain "
                            "'default_value' and 'unit' keys."
                        )

    def validate_dataframe_indices(
        self, name: str, df: DataFrame, allowed_names: set
    ) -> None:
        """Validate DataFrame index names against allowed values.

        Args:
            name: The name of the attribute being validated.
            df: The DataFrame to validate.
            allowed_names: Set of allowed index names.

        Raises:
            ValueError: If any index name is not in the allowed set.
        """
        invalid_indices = set(df.index.names) - allowed_names
        if invalid_indices:
            raise ValueError(
                f"Invalid index names {invalid_indices} in attribute '{name}'. "
                f"Allowed names are: {', '.join(sorted(allowed_names))}."
            )

    def validate_min_max(self, name: str, value: float | list | DataFrame):
        """
        Validate that a min/max value is in the interval [0, 1].

        Args:
            name: The name of the attribute being validated.
            value: The min/max value to validate.
        """
        self._validate_min(name, value)
        self._validate_max(name, value)

    def _validate_min(self, name: str, value: float | list | DataFrame):
        """Validate that a value is above the minimum value."""
        if self.minimum_value is None:
            return

        if isinstance(value, (int, float)):
            if value < self.minimum_value:
                raise ValueError(
                    f"Attribute '{name}' must be >={self.minimum_value}, got {value}."
                )
        elif isinstance(value, list):
            for i, v in enumerate(value):
                if v < self.minimum_value:
                    raise ValueError(
                        f"Attribute '{name}' list values must be "
                        f">={self.minimum_value}, got value {v} at index {i}."
                    )
        elif hasattr(value, "min"):
            if (value.min() < self.minimum_value).any():
                raise ValueError(
                    f"Attribute '{name}' DataFrame values must be "
                    f">={self.minimum_value}, got minimum value {value.min()}."
                )
        else:
            raise TypeError(
                f"Attribute '{name}' must be a float, list, or DataFrame, "
                f"got {type(value).__name__}."
            )

    def _validate_max(self, name: str, value: float | list | DataFrame):
        """Validate that a value is below the maximum value."""
        if self.maximum_value is None:
            return

        if isinstance(value, (int, float)):
            if value > self.maximum_value:
                raise ValueError(
                    f"Attribute '{name}' must be <={self.maximum_value}, got {value}."
                )
        elif isinstance(value, list):
            for i, v in enumerate(value):
                if v > self.maximum_value:
                    raise ValueError(
                        f"Attribute '{name}' list values must be "
                        f"<={self.maximum_value}, got value {v} at index {i}."
                    )
        elif hasattr(value, "max"):
            if (value.max() > self.maximum_value).any():
                raise ValueError(
                    f"Attribute '{name}' DataFrame values must be "
                    f"<={self.maximum_value}, got maximum value {value.max()}."
                )
        else:
            raise TypeError(
                f"Attribute '{name}' must be a float, list, or DataFrame, "
                f"got {type(value).__name__}."
            )
