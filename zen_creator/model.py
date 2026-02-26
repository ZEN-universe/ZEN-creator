from functools import cached_property
from pathlib import Path
from typing import Type

from zen_creator.elements.element import Element
from zen_creator.elements.energy_system import EnergySystem
from zen_creator.elements import (
    Technology,
    Carrier,
    ConversionTechnology,
    TransportTechnology,
    StorageTechnology,
    RetrofittingTechnology,
    EnergySystem,
)


from zen_creator.sectors import Sector
from zen_creator.utils.default_config import Config, load_config
from zen_creator.utils.system_file import SystemFile
import shutil


class Model:
    def __init__(self, config: Config | None = None):

        # set attributes from input arguments
        self.config: Config = config if config is not None else Config()
        self.name: str = self.config.name
        self.output_folder: Path = Path(self.config.main_settings.output_folder)
        self.source_path: Path | None = (
            Path(self.config.main_settings.source_path)
            if self.config.main_settings.source_path is not None
            else None
        )

        # initialize other attributes
        self.energy_system: EnergySystem | None = EnergySystem(self)
        self.elements: dict[str, Element] = dict()

        for sector in self.config.sector_settings.sectors:
            self.add_sector_by_name(sector)

        for element in self.config.sector_settings.elements:
            self.add_element_by_name(element)

        for element in self.config.sector_settings.elements_remove:
            self.remove_element_by_name(element)

    # -------- Constructors --------------------------------------------------------

    @classmethod
    def from_config(cls, config_path: Path):
        """
        Construct model from a configuration file.

        Also includes the building of the model, i.e. setting all attributes of
        all elements based on the config file.

        :param config: Description
        :type config: Config
        """

        raise NotImplementedError(
            "Model construction from config file path is " "is not implemented yet."
        )
        name = "model_1"  # ToDo - fix once config structure finalized
        out_path = Path(".")
        model = cls(name, out_path)
        model.config = load_config(config_path)["model_1"]  # ToDo fix config loading
        #        model.energy_system = EnergySystem(model)
        for sector in model.config.sector_settings.sectors:
            model.add_sector(sector)
        model.build()
        return model

    @classmethod
    def from_existing(
        cls, existing_model_path: Path | str, config: Config | None = None
    ):
        """
        Construct model from an existing model.

        # ToDo
        """
        existing_model_path = Path(existing_model_path)
        if not existing_model_path.exists():
            raise ValueError(f"Input path '{existing_model_path}' does not exist.")

        # construct model
        model = cls(config=config)

        # overwrite default values with values from existing model
        print(
            f"Overwrite attributes using existing "
            f"model {existing_model_path} ----------"
        )
        model.energy_system.overwrite_from_existing_model(existing_model_path)
        for element in model.elements.values():
            element.overwrite_from_existing_model(existing_model_path)

        return model

    # -------- Properties ----------------------------------------------------------
    @cached_property
    def energy_system(self):
        return EnergySystem(self)

    @property
    def carriers(self):
        """
        Returns dictionary of all carriers in the current model.
        """
        return {
            name: element
            for (name, element) in self.elements.items()
            if isinstance(element, Carrier)
        }

    @property
    def technologies(self):
        return {
            name: element
            for (name, element) in self.elements.items()
            if isinstance(element, Technology)
        }

    @property
    def storage_technologies(self):
        return {
            name: element
            for (name, element) in self.elements.items()
            if isinstance(element, StorageTechnology)
        }

    @property
    def conversion_technologies(self):
        return {
            name: element
            for (name, element) in self.elements.items()
            if isinstance(element, ConversionTechnology)
        }

    @property
    def transport_technologies(self):
        return {
            name: element
            for (name, element) in self.elements.items()
            if isinstance(element, TransportTechnology)
        }

    @property
    def retrofitting_technologies(self):
        return {
            name: element
            for (name, element) in self.elements.items()
            if isinstance(element, RetrofittingTechnology)
        }

    @property
    def output_path(self):
        """
        Output path where model will be saved.
        """
        output_path = self.output_folder / self.name

        # ensure directory exists
        output_path.mkdir(parents=True, exist_ok=True)

        return output_path

    @property
    def output_folder(self):
        """
        Output folder where model will be saved.
        """
        return self._out_path

    @output_folder.setter
    def output_folder(self, value):
        """
        Validates output path.
        """
        if not isinstance(value, Path):
            raise TypeError(
                f"Expected an instance of 'Path', got"
                f"'{type(value).__name__}' instead."
            )
        self._out_path = value

    @property
    def source_path(self):
        """
        Source path where model data is read from.
        """
        return self._source_path

    @source_path.setter
    def source_path(self, value):
        """
        Validates source path.
        """
        if value is None:
            self._source_path = value
            return
        if not isinstance(value, Path):
            raise TypeError(
                f"Expected an instance of 'Path' or `None`, got"
                f"'{type(value).__name__}' instead."
            )
        if not value.exists():
            raise ValueError(f"Source path '{value}' does not exist.")
        self._source_path = value

    # -------- Adding / Removing Elements  -----------------------------------------

    def add_element_by_name(self, element: str):
        """
        ToDo.
        """
        if not isinstance(element, str):
            raise TypeError(
                f"Expected a subclass of 'str', "
                f"got '{type(element).__name__}' instead."
            )

        element_cls = Element._element_registry.setdefault(element, None)
        if element_cls is None:
            raise ValueError(f"Element '{element}' is not registered.")

        self.add_element(element_cls)

        return

    def add_element(self, element_cls: Type[Element]):
        """
        Adds an element to the model.
        """
        # check that element is valid
        if element_cls is None or not issubclass(element_cls, Element):
            raise TypeError(
                f"Expected an subclass of 'Element', got"
                f"'{type(element_cls).__name__}' instead."
            )

        # initialize element
        element = element_cls(model=self)

        print(f"Add element {element.name}")

        # add (name, element) pair to model.elements
        if element.name not in self.elements:
            self.elements[element.name] = element
        else:
            print(f"Element '{element.name}' already exists in the dictionary.")

        return

    def remove_element(self, element_cls: Type[Element]):
        """
        Removes an element from the model.
        """
        if not isinstance(element_cls, type) or not issubclass(element_cls, Element):
            raise TypeError(
                f"Expected a subclass of 'Element', "
                f"got '{type(element_cls).__name__}' instead."
            )

        # Find matching element names
        matches = [
            name
            for name, element in self.elements.items()
            if isinstance(element, element_cls)
        ]

        if not matches:
            print(f"No element of type '{element_cls.__name__}' found in the model.")
            return

        if len(matches) > 1:
            raise ValueError(
                f"Multiple elements of type '{element_cls.__name__}' found in "
                "the model."
            )

        name = matches[0]

        # remove element
        self.remove_element_by_name(name)

    def remove_element_by_name(self, name: str):

        print(f"Remove element {name}")
        del self.elements[name]

    def add_sector_by_name(self, sector: str):
        """
        ToDo.
        """
        if not isinstance(sector, str):
            raise TypeError(
                f"Expected a subclass of 'str', "
                f"got '{type(sector).__name__}' instead."
            )

        sector_cls = Sector._sector_registry.setdefault(sector, None)
        if sector_cls is None:
            raise ValueError(f"Sector '{sector}' is not registered.")

        self.add_sector(sector_cls)

        return

    def add_sector(self, sector_cls: Type[Sector]):
        """
        ToDo.
        """
        if not isinstance(sector_cls, type) or not issubclass(sector_cls, Sector):
            raise TypeError(
                f"Expected a subclass of 'Sector', "
                f"got '{type(sector_cls).__name__}' instead."
            )

        print(f"Add sector: {sector_cls.name} --------")

        for element in sector_cls().elements:
            self.add_element(element)

        return

    def remove_sector(self, sector_cls: Type[Sector]):
        """
        Todo
        """
        if not isinstance(sector_cls, type) or not issubclass(sector_cls, Sector):
            raise TypeError(
                f"Expected a subclass of 'Sector', "
                f"got '{type(sector_cls).__name__}' instead."
            )

        print(f"Remove sector: {sector_cls.name} --------")

        for element in sector_cls().elements:
            self.remove_element(element)

    # ------- Building model ---------------------------------------------------

    def build(self):
        """
        Builds the model by calling build() method of all elements.
        """
        print("Build model --------")

        # build energy system first
        self.energy_system.build()

        # build carriers and technologies
        for element in self.elements.values():
            element.build()

    # -------- Write model -----------------------------------------------------

    def write(self):
        # verify completeness
        self.validate()

        # remove output path if it exists
        if self.output_path.exists():
            print(f"Output path {self.output_path} aready exists. Deleting "
                  "existing contents.")
            shutil.rmtree(self.output_path)

        # write system.json
        SystemFile(self).write()

        # write energy system folder
        self.energy_system.write()

        # save all elements (technologies and carriers)
        for element in self.elements.values():
            element.write()

        print("Done")

    # -------- Validate model ------------------------------------------------------

    def validate(self):
        # check that all carriers of technologies are defined
        self._chech_energy_system()
        self._check_carriers()

    def _chech_energy_system(self):
        """
        Verifies that the energy system is complete, i.e. that all technologies
        and carriers are included in the energy system.
        """
        if self.energy_system is None:
            raise ValueError("Energy system is not defined.")

    def _check_carriers(self):
        """
        Verifies the carriers in the model.

        Checks the following:

        - each technology only has one reference carrier
        - the reference carrier of a technology is either an input or an output
          carrier
        - all carriers used in technologies are defined in the model.
        """
        # ToDo -- consider moving some of these to setters
        carriers = set()
        for technology in self.technologies.values():
            reference_carrier = set(technology.reference_carrier.default_value)

            if len(reference_carrier) != 1:
                raise ValueError(
                    f"Technology {technology.name} is expected to have only "
                    f"one reference carrier, got {len(reference_carrier)}"
                )

            carriers = carriers.union(reference_carrier)
        
        for technology in self.conversion_technologies.values():
            input_carriers = set(technology.input_carrier.default_value)
            output_carriers = set(technology.output_carrier.default_value)
            reference_carrier = set(technology.reference_carrier.default_value)

            tech_carriers = input_carriers.union(output_carriers)

            if not reference_carrier.issubset(tech_carriers):
                raise ValueError(
                    f"The reference carriers for technology {technology.name} "
                    "must be one of the input or output carriers. Expected "
                    f"one of {tech_carriers}, got {reference_carrier}."
                )

            carriers = carriers.union(tech_carriers)

        if not carriers.issubset(set(self.carriers)):
            raise ValueError(
                f"The following carriers, used by technologies, are not "
                f"missing from the model {carriers.difference(self.carriers)}."
            )
