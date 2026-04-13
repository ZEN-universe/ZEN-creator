from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass
from abc import ABC
from typing import Type

from zen_creator.elements import Element


class Sector(ABC):
    name: str
    _sector_registry: dict[str, Type[Sector]] = {}

    def __init__(self) -> None:
        self._elements: list[type[Element]] = []

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "name"):
            raise Exception(
                f"Subclass {cls.__name__} should define a class variable " "" "'name'."
            )
        Sector._sector_registry[cls.name] = cls

    def __repr__(self) -> str:
        """
        Control how class will be displayed. Overwritting since singleton.
        """
        return f"<Sector {self.name}>"

    @property
    def elements(self) -> list[Type[Element]]:
        return self._elements

    @elements.setter
    def elements(self, v: list[type[Element]]) -> None:
        """
        Validates elements each time it is set.

        - checks that it is a list
        - checks that all items in the list are subclasses of Element
        """
        if not isinstance(v, list):
            raise TypeError(f"Expected object of type `list`, got {type(v)}")
        for element in v:
            if not issubclass(element, Element):
                raise TypeError(f"Expected subclass of `Element`, got {type(element)}")
        self._elements = v
