from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass
from abc import ABC
from typing import Type

import zen_creator.elements.carriers as carriers
import zen_creator.elements.conversion_technologies as conversion_technologies
import zen_creator.elements.storage_technologies as storage_technologies
import zen_creator.elements.transport_technologies as transport_technologies
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


class Electricity(Sector):
    name = "electricity"

    def __init__(self) -> None:
        super().__init__()
        self.elements = [
            carriers.Electricity,  # type: ignore[attr-defined]
            carriers.Heat,  # type: ignore[attr-defined]
            carriers.Lignite,  # type: ignore[attr-defined]
            conversion_technologies.Photovoltaics,  # type: ignore[attr-defined]
            conversion_technologies.LigniteCoalPlant,  # type: ignore[attr-defined]
            storage_technologies.PumpedHydro,  # type: ignore[attr-defined]
            transport_technologies.PowerLine,  # type: ignore[attr-defined]
        ]


class Heat(Sector):
    name = "heat"

    def __init__(self) -> None:
        super().__init__()
        self.elements = [
            carriers.Heat,  # type: ignore[attr-defined]
            conversion_technologies.HeatPump,  # type: ignore[attr-defined]
            conversion_technologies.ElectrodeBoiler,  # type: ignore[attr-defined]
        ]


class PassengerTransport(Sector):
    name = "passenger_transport"

    def __init__(self) -> None:
        super().__init__()


class TruckTransport(Sector):
    name = "truck_transport"

    def __init__(self) -> None:
        super().__init__()


class Shipping(Sector):
    name = "shipping"

    def __init__(self) -> None:
        super().__init__()


class Aviation(Sector):
    name = "aviation"

    def __init__(self) -> None:
        super().__init__()


class Refining(Sector):
    name = "refining"

    def __init__(self) -> None:
        super().__init__()


class Hydrogen(Sector):
    name = "hydrogen"

    def __init__(self) -> None:
        super().__init__()


class Methanol(Sector):
    name = "methanol"

    def __init__(self) -> None:
        super().__init__()


class Ammonia(Sector):
    name = "ammonia"

    def __init__(self) -> None:
        super().__init__()


class Carbon(Sector):
    name = "carbon"

    def __init__(self) -> None:
        super().__init__()


class Cement(Sector):
    name = "cement"

    def __init__(self) -> None:
        super().__init__()


class Steel(Sector):
    name = "steel"

    def __init__(self) -> None:
        super().__init__()
