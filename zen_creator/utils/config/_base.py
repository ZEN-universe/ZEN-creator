from typing import Any

from pydantic import BaseModel, ConfigDict


class Subscriptable(BaseModel):
    """
    Allows dictionary-like access to class attributes.
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    def __getitem__(self, __name: str) -> Any:
        return getattr(self, __name)

    def __setitem__(self, __name: str, __value: Any) -> None:
        setattr(self, __name, __value)

    def keys(self) -> Any:
        return self.model_dump().keys()

    def items(self) -> Any:
        return self.model_dump().items()

    def values(self) -> Any:
        return self.model_dump().values()
