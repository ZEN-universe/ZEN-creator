import json
from pathlib import Path

from pydantic import Field

from ._base import Subscriptable


class ElementTypeList(Subscriptable):
    """Config for list of elements by type."""

    energy_system: str = ""
    set_sectors: list[str] = Field(default_factory=list)
    set_conversion_technologies: list[str] = Field(default_factory=list)
    set_storage_technologies: list[str] = Field(default_factory=list)
    set_transport_technologies: list[str] = Field(default_factory=list)
    set_retrofitting_technologies: list[str] = Field(default_factory=list)
    set_carriers: list[str] = Field(default_factory=list)

    @classmethod
    def load_from_existing_model(
        cls, existing_model_path: Path | str
    ) -> "ElementTypeList":
        model_path = Path(existing_model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"{model_path} does not exist")

        system_path = model_path / "system.json"
        if not system_path.is_file():
            raise FileNotFoundError(f"could not find {system_path}")

        system_dict = json.loads(system_path.read_text())

        et = cls()
        for field in (
            "set_conversion_technologies",
            "set_storage_technologies",
            "set_transport_technologies",
            "set_retrofitting_technologies",
        ):
            setattr(et, field, system_dict.get(field, []))

        et.set_carriers = cls._infer_carriers(model_path, et)
        return et

    @staticmethod
    def _infer_carriers(model_path: Path, et: "ElementTypeList") -> list[str]:
        carriers: set[str] = set()

        tech_map = {
            "set_conversion_technologies": ("set_conversion_technologies", True),
            "set_retrofitting_technologies": (
                "set_conversion_technologies/set_retrofitting_technologies",
                True,
            ),
            "set_storage_technologies": ("set_storage_technologies", False),
            "set_transport_technologies": ("set_transport_technologies", False),
        }

        for attr, (subfolder, has_io) in tech_map.items():
            for tech in getattr(et, attr):
                attr_file = (
                    model_path
                    / "set_technologies"
                    / subfolder
                    / tech
                    / "attributes.json"
                )
                if not attr_file.is_file():
                    raise FileNotFoundError(
                        f"attributes for {tech!r} not found at {attr_file}"
                    )
                data = json.loads(attr_file.read_text())

                carriers |= set(
                    data.get("reference_carrier", {}).get("default_value", [])
                )
                if has_io:
                    carriers |= set(
                        data.get("input_carrier", {}).get("default_value", [])
                    )
                    carriers |= set(
                        data.get("output_carrier", {}).get("default_value", [])
                    )

        return sorted(carriers)


class ElementConfig(Subscriptable):
    """Config for element settings."""

    insert: ElementTypeList = Field(default_factory=ElementTypeList)
    exclude: ElementTypeList = Field(default_factory=ElementTypeList)
