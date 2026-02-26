from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass
from abc import ABC
from typing import Type

from zen_creator.elements import Element
import zen_creator.elements.conversion_technologies as conversion_technologies
import zen_creator.elements.storage_technologies as storage_technologies
import zen_creator.elements.transport_technologies as transport_technologies
import zen_creator.elements.carriers as carriers


class Sector(ABC):
    name: str
    _sector_registry: dict[str, Type[Sector]] = {}

    def __init__(self):
        self._elements = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "name"):
            raise Exception(
                f"Subclass {cls.__name__} should define a class variable " "" "'name'."
            )
        Sector._sector_registry[cls.name] = cls

    def __repr__(self):
        """
        Control how class will be displayed. Overwritting since singleton.
        """
        return f"<Sector {self.name}>"

    @property
    def elements(self) -> list[Type[Element]]:
        return self._elements

    @elements.setter
    def elements(self, v):
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

    def __init__(self):
        super().__init__()
        self.elements = [
            carriers.Electricity,
            carriers.Heat,
            carriers.Lignite,
            conversion_technologies.Photovoltaics,
            conversion_technologies.LigniteCoalPlant,
            storage_technologies.PumpedHydro,
            transport_technologies.PowerLine
        ]


class Heat(Sector):
    name = "heat"

    def __init__(self):
        super().__init__()
        self.elements = [
            carriers.Heat,
            conversion_technologies.HeatPump,
            conversion_technologies.ElectrodeBoiler,
        ]


class PassengerTransport(Sector):
    name = "passenger_transport"

    def __init__(self):
        super().__init__()


class TruckTransport(Sector):
    name = "truck_transport"

    def __init__(self):
        super().__init__()


class Shipping(Sector):
    name = "shipping"

    def __init__(self):
        super().__init__()


class Aviation(Sector):
    name = "aviation"

    def __init__(self):
        super().__init__()


class Refining(Sector):
    name = "refining"

    def __init__(self):
        super().__init__()


class Hydrogen(Sector):
    name = "hydrogen"

    def __init__(self):
        super().__init__()


class Methanol(Sector):
    name = "methanol"

    def __init__(self):
        super().__init__()


class Ammonia(Sector):
    name = "ammonia"

    def __init__(self):
        super().__init__()


class Carbon(Sector):
    name = "carbon"

    def __init__(self):
        super().__init__()


class Cement(Sector):
    name = "cement"

    def __init__(self):
        super().__init__()


class Steel(Sector):
    name = "steel"

    def __init__(self):
        super().__init__()
