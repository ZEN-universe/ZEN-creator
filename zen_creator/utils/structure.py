from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any

from zen_creator.elements import (
    Carrier,
    ConversionTechnology,
    RetrofittingTechnology,
    StorageTechnology,
    TransportTechnology,
)
from zen_creator.sectors import Sector

if TYPE_CHECKING:
    from zen_creator.model import Model

# technology types, most specific first since retrofitting technologies are
# also conversion technologies
TECHNOLOGY_TYPES = {
    "retrofitting_technology": RetrofittingTechnology,
    "conversion_technology": ConversionTechnology,
    "storage_technology": StorageTechnology,
    "transport_technology": TransportTechnology,
}

CARRIER_ATTRIBUTES = [
    "reference_carrier",
    "input_carrier",
    "output_carrier",
    "retrofit_reference_carrier",
]


def model_structure(model: Model) -> dict[str, Any]:
    """Return the sectors, technologies and carriers of a model and how they connect.

    Only the carrier attributes of the technologies are built, so the model does
    not need to be built and no raw data is read.

    Returns:
        dict: With the keys "sectors", "technologies", "carriers" and
            "carrier_flows". Sectors map to their description, required sectors and
            elements. Technologies map to their type, sectors, carriers and, for
            retrofitting technologies, base technology. Carriers map to their
            sectors and the technologies that produce, consume, store or transport
            them. Carrier flows list the carriers that are converted into each
            other (see :func:`carrier_flows`).
    """
    element_sectors: dict[str, list[str]] = {}
    sectors = {}
    for name in sorted(model.sectors):
        sector_cls = Sector._sector_registry[name]
        elements = [
            element.name
            for element in sector_cls().elements
            if element.name in model.elements
        ]
        for element in elements:
            element_sectors.setdefault(element, []).append(name)
        sectors[name] = {
            "description": inspect.getdoc(sector_cls) or "",
            "required_sectors": list(sector_cls.required_sectors),
            "elements": elements,
        }

    carriers = {
        name: {
            "sectors": element_sectors.get(name, []),
            "produced_by": [],
            "consumed_by": [],
            "stored_by": [],
            "transported_by": [],
        }
        for name, carrier in model.elements.items()
        if isinstance(carrier, Carrier)
    }

    technologies = {}
    for name, technology in model.technologies.items():
        technology_type = next(
            key for key, cls in TECHNOLOGY_TYPES.items() if isinstance(technology, cls)
        )
        entry: dict[str, Any] = {
            "type": technology_type,
            "sectors": element_sectors.get(name, []),
        }
        for attribute in CARRIER_ATTRIBUTES:
            if hasattr(technology, attribute):
                entry[attribute] = list(getattr(technology, attribute).default_value)
        if isinstance(technology, RetrofittingTechnology):
            entry["base_technology"] = technology.base_technology_name
        technologies[name] = entry

        if technology_type == "storage_technology":
            roles = {"stored_by": entry["reference_carrier"]}
        elif technology_type == "transport_technology":
            roles = {"transported_by": entry["reference_carrier"]}
        else:
            roles = {
                "consumed_by": entry["input_carrier"],
                "produced_by": entry["output_carrier"],
            }
        for role, carrier_names in roles.items():
            for carrier in carrier_names:
                if carrier in carriers:
                    carriers[carrier][role].append(name)

    return {
        "sectors": sectors,
        "technologies": technologies,
        "carriers": carriers,
        "carrier_flows": carrier_flows(technologies),
    }


def carrier_flows(technologies: dict[str, dict[str, Any]]) -> list[tuple[str, str]]:
    """Return the pairs of carriers that are converted into each other.

    A conversion technology converts each of its input carriers into each of its
    output carriers.

    Returns:
        list[tuple[str, str]]: Sorted pairs of input and output carrier.
    """
    flows = {
        (source, target)
        for technology in technologies.values()
        if "input_carrier" in technology
        for source in technology["input_carrier"]
        for target in technology["output_carrier"]
        if source != target
    }
    return sorted(flows)
