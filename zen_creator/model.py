import json
import shutil
from pathlib import Path
from typing import Iterable, Optional, Type

from zen_creator.elements import (
    Carrier,
    ConversionTechnology,
    EnergySystem,
    GenericCarrier,
    GenericConversionTechnology,
    GenericEnergySystem,
    GenericRetrofittingTechnology,
    GenericStorageTechnology,
    GenericTransportTechnology,
    RetrofittingTechnology,
    StorageTechnology,
    Technology,
    TransportTechnology,
)
from zen_creator.elements.element import Element
from zen_creator.sectors import Sector
from zen_creator.utils.default_config import Config


class Model:
    """Structured representation of the ZEN-garden input data.

    This class stores the input data for the ZEN-garden energy system
    model in a structured way. It provides methods to build, modify,
    validate, and write the model to the input data.

    Attributes:
        config (Config): The configuration object for the model.
        name (str): The name of the model.
        output_folder (Path): The folder where the model output will be saved.
        source_path (Path): The path to the source data.
        energy_system (EnergySystem): Object representing all data in the
            "energy_system" folder of the ZEN-garden input data.
        elements (dict[str, Element]): Dictionary of elements (carriers and
            technologies) present in the model.
    """

    def __init__(self) -> None:
        """Initialize a new Model instance."""

        # internal variables for properties
        self.config: Config = Config()
        self.name: str = self.config.name
        self._output_folder: Optional[Path] = None
        self._source_path: Optional[Path] = None
        self._energy_system: Optional[EnergySystem] = None

        # initialize other attributes
        self.elements: dict[str, Element] = {}

    @classmethod
    def from_config(cls, config: Config | str | Path):
        """Initialize a new Model instance.

        Args:
            config (Config | str | Path): The configuration for the model.
                Can be a Config object, or a path to a config file.

        Raises:
            TypeError: If config is not a valid type.
        """
        # set attributes from input arguments
        model = cls()

        model.config = (
            config if isinstance(config, Config) else Config.load_from_yaml(config)
        )
        model.name = model.config.name
        model.output_folder = model.config.output_folder
        model.source_path = model.config.source_path

        # initialize other attributes
        model.energy_system = GenericEnergySystem(model)
        model.elements = dict()

        insert = model.config.elements.insert
        exclude = model.config.elements.exclude

        # Add sectors (using a loop directly)
        for sector in insert.set_sectors:
            model.add_sector_by_name(sector)

        # Add technologies by iterating over the technology types
        element_map = {
            "set_conversion_technologies": "conversion_technology",
            "set_storage_technologies": "storage_technology",
            "set_transport_technologies": "transport_technology",
            "set_retrofitting_technologies": "retrofitting_technology",
            "set_carriers": "carrier",
        }
        for element_set, element_type in element_map.items():
            element_list = getattr(insert, element_set)
            for element in element_list:
                model.add_element_by_name(element, element_type)

        # Remove sectors that should be excluded
        # ToDo:

        # Remove technologies that should be excluded
        for element_set in element_map.keys():
            element_list = getattr(exclude, element_set)
            for element in element_list:
                model.remove_element_by_name(element)

        return model

    @classmethod
    def from_existing(
        cls, existing_model_path: Path | str, config: Config | str | Path | None = None
    ):
        """Construct a model from an ZEN-garden input folder.

        This method loads the data of an existing ZEN-garden model
        into the data structure. The existing model must be in the
        proper data format for ZEN-garden.

        If not config is specified, a configuration file is created from
        the default configurations. The system configurations, unit
        unit configurations, model name, and output folder are then taken
        directly from the

        This function performs the following steps:
            1. Create a Model object using the configuration file. This
               object only has the elements (technologies and carriers)
               specified in the configurations.
            2. Overwrite the Model elements using data from the existing
               model. Once again, only elements specified in the
               configuration file are included in the model.

        Args:
            existing_model_path (Path | str): Path to the existing model.
            config (Config | str | Pat | None): Configuration file for the
                new model.Can be a Config object, or a path to a
                config file. If a configuration file is created from the default
                configurations. The name

        Returns:
            Model: A new Model instance initialized from the existing model.

        Raises:
            ValueError: If the existing model path does not exist.
        """
        existing_model_path = Path(existing_model_path)

        if not existing_model_path.exists():
            raise ValueError(f"Input path '{existing_model_path}' does not exist.")

        # handle config
        if config is None:
            config = Config.load_from_existing_model(existing_model_path)

        # construct model object
        # no data is loaded yet, only default values form zen-creator are used.
        model = cls.from_config(config)

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
    @property
    def carriers(self) -> dict[str, Carrier]:
        """
        Returns dictionary of all carriers in the current model.

        Returns:
            dict[str, Carrier]: Mapping of carrier names to
                Carrier objects.
        """
        return {
            name: element
            for (name, element) in self.elements.items()
            if isinstance(element, Carrier)
        }

    @property
    def technologies(self) -> dict[str, Technology]:
        """Dictionary of all technologies in the current model.

        Returns:
            dict[str, Technology]: Mapping of technology names to
                Technology objects.
        """
        return {
            name: element
            for (name, element) in self.elements.items()
            if isinstance(element, Technology)
        }

    @property
    def storage_technologies(self) -> dict[str, StorageTechnology]:
        """Dictionary of all storage technologies in the current model.

        Returns:
            dict[str, StorageTechnology]: Mapping of storage technology
                names to objects.
        """
        return {
            name: element
            for (name, element) in self.elements.items()
            if isinstance(element, StorageTechnology)
        }

    @property
    def conversion_technologies(self) -> dict[str, ConversionTechnology]:
        """Dictionary of all conversion technologies in the current model.

        Returns:
            dict[str, ConversionTechnology]: Mapping of conversion
                technology names to objects.
        """
        return {
            name: element
            for (name, element) in self.elements.items()
            if isinstance(element, ConversionTechnology)
        }

    @property
    def transport_technologies(self) -> dict[str, TransportTechnology]:
        """Dictionary of all transport technologies in the current model.

        Returns:
            dict[str, TransportTechnology]: Mapping of transport
                technology names to objects.
        """
        return {
            name: element
            for (name, element) in self.elements.items()
            if isinstance(element, TransportTechnology)
        }

    @property
    def retrofitting_technologies(self) -> dict[str, RetrofittingTechnology]:
        """Dictionary of all retrofitting technologies in the current model.

        Returns:
            dict[str, RetrofittingTechnology]: Mapping of retrofitting
                technology names to objects.
        """
        return {
            name: element
            for (name, element) in self.elements.items()
            if isinstance(element, RetrofittingTechnology)
        }

    @property
    def energy_system(self) -> EnergySystem:
        """Return EnergySystem class of the model.

        Returns:
            EnergySystem: Object containing all energy system configurations
                of the model.
        Raises:
            ValueError: If no energy system has been defined.
        """
        if not self._energy_system:
            raise ValueError("The energy system has not been defined yet.")
        return self._energy_system

    @energy_system.setter
    def energy_system(self, value: EnergySystem | None) -> None:
        """Set the energy_system and validate the input.

        Args:
            value (EnergySystem | None): The path energy_system.

        Raises:
            TypeError: If value is not a EnergySystem instance or None.
        """
        if not isinstance(value, EnergySystem) and value is not None:
            raise ValueError("The energy system has not been defined yet")
        self._energy_system = value

    @property
    def output_path(self) -> Path:
        """
        Output path where model will be saved.

        The output path consists of the output folder specified in the
        configurations and the model name.

        Side effects:
            Creates the folder corresponding to the output path if it
            does not exist.
        """
        if self.output_folder is None:
            raise ValueError("Output folder has not been set yet.")

        output_path = self.output_folder / self.name

        # ensure directory exists
        output_path.mkdir(parents=True, exist_ok=True)

        return output_path

    @property
    def output_folder(self) -> Path:
        """
        Output folder where model will be saved.
        """
        if self._out_path is None:
            raise ValueError("The output folder has not been set yet.")
        return self._out_path

    @output_folder.setter
    def output_folder(self, value: Path | str | None):
        """Set the output folder and validate the input.

        Args:
            value (Path): The path to the output folder.

        Raises:
            TypeError: If value is not a Path instance.
        """
        if value is None:
            self._out_path = value
            return
        if not isinstance(value, (Path, str)):
            raise TypeError(
                f"Expected an instance of 'Path', 'str', or 'None', got"
                f"'{type(value).__name__}' instead."
            )
        self._out_path = Path(value)

    @property
    def source_path(self) -> Path:
        """
        Source path where model data is read from.
        """
        if self._source_path is None:
            raise ValueError("The source path has not been set yet.")
        return self._source_path

    @source_path.setter
    def source_path(self, value: Path | str | None):
        """Set the source path and validate the input.

        Args:
            value (Path): The path to the source data.

        Raises:
            TypeError: If value is not a Path instance.
            ValueError: If the path does not exist.
        """
        # handle None
        if value is None:
            self._source_path = value
            return

        # check type str or Path
        if not isinstance(value, (Path, str)):
            raise TypeError(
                f"Expected an instance of 'Path', 'str' or 'None', got"
                f"'{type(value).__name__}' instead."
            )

        # check whether file exists
        source_path = Path(value)
        if not source_path.exists():
            raise ValueError(f"Source path '{value}' does not exist.")

        # save
        self._source_path = source_path

    # -------- Adding / Removing Elements  -----------------------------------------

    def add_element_by_name(
        self, element_name: str, generic: None | str = None
    ) -> None:
        """Add an element to the model by its name.

        Args:
            element (str): The name of the element to add.

        Raises:
            TypeError: If element is not a string.
            ValueError: If the element is not registered. Elements get
                registered when their class definitions are imported.
        """
        generic_map: dict[
            str,
            Type[GenericConversionTechnology]
            | Type[GenericStorageTechnology]
            | Type[GenericTransportTechnology]
            | Type[GenericRetrofittingTechnology]
            | Type[GenericCarrier],
        ] = {
            "conversion_technology": GenericConversionTechnology,
            "storage_technology": GenericStorageTechnology,
            "transport_technology": GenericTransportTechnology,
            "retrofitting_technology": GenericRetrofittingTechnology,
            "carrier": GenericCarrier,
        }

        # Validate inputs
        if not isinstance(element_name, str):
            raise TypeError(
                f"Expected a subclass of 'str', "
                f"got '{type(element_name).__name__}' instead."
            )
        if generic is not None and generic not in generic_map.keys():
            raise ValueError(
                f"Expected 'element_type' to be one of None or {generic_map.keys()}."
            )

        if element_name in self.elements:
            print(f"Element '{element_name}' already exists in the dictionary.")
            return

        # Get type class and generic class
        if (subtype_cls := Element.get_by_name(element_name)) is not None:
            # initialize element via defined subclass if it exists
            element = subtype_cls(model=self)
        elif generic is not None:
            # initialize element via generic type
            generic_cls = generic_map[generic]
            element = generic_cls(model=self, name=element_name)
        else:
            raise ValueError(
                f"No class definition found for element {element_name}."
                "Please verify that this class definition exists and has"
                "been imported."
            )

        # add to element list
        self.elements[element_name] = element

        return

    def add_element(self, element_cls: Type[Element]) -> None:
        """Add an element to the model.

        Args:
            element_cls (Type[Element]): The element class to
                instantiate and add.

        Raises:
            TypeError: If element_cls is not a subclass of Element.
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

    def remove_element(self, element_cls: Type[Element]) -> None:
        """
        Removes an element from the model.

        Args:
            element_cls (Type[Element]): The element class to
                remove.
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
                "the model. Use 'Model.remove_element_by_name()' to specify which"
                "specific element to remove."
            )

        name = matches[0]

        # remove element
        self.remove_element_by_name(name)

    def remove_element_by_name(self, name: str) -> None:
        """Remove an element from the model by its name.

        Args:
            name (str): The name of the element to remove.
        """
        print(f"Remove element {name}")
        del self.elements[name]

    def add_sector_by_name(self, sector: str) -> None:
        """Add a sector to the model by its name.

        Args:
            sector (str): The name of the sector to add.

        Raises:
            TypeError: If sector is not a string.
            ValueError: If the sector is not registered.
        """
        if not isinstance(sector, str):
            raise TypeError(
                f"Expected a subclass of 'str', "
                f"got '{type(sector).__name__}' instead."
            )

        sector_cls = Sector._sector_registry.get(sector)

        if sector_cls is None:
            raise ValueError(f"Sector '{sector}' is not registered.")

        self.add_sector(sector_cls)

        return

    def add_sector(self, sector_cls: Type[Sector]) -> None:
        """Add a sector to the model.

        Args:
            sector_cls (Type[Sector]): The sector class to add.

        Raises:
            TypeError: If sector_cls is not a subclass of Sector.
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

    def remove_sector(self, sector_cls: Type[Sector]) -> None:
        """Remove a sector from the model.

        Args:
            sector_cls (Type[Sector]): The sector class to remove.

        Raises:
            TypeError: If sector_cls is not a subclass of Sector.
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

    def build(self) -> None:
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

    def write(self) -> None:
        """Write the model to disk.

        This method validates the model, removes any existing output directory,
        writes the system file, and saves all elements.
        """
        # verify completeness
        self.validate()

        # remove output path if it exists
        if self.output_path.exists():
            print(
                f"Output path {self.output_path} already exists. Deleting "
                "existing contents."
            )
            shutil.rmtree(self.output_path)

        # write system.json
        self.write_system_file()

        # write energy system folder
        self.energy_system.write()

        # save all elements (technologies and carriers)
        for element in self.elements.values():
            element.write()

        print("Done")

    def write_system_file(self) -> None:
        """Write the system.json file for the model.

        This method generates the system configuration dictionary and writes it
        to system.json in the output directory.
        """
        # convert the Pydantic model instance to a dictionary
        system_json = self.config.system.model_dump(exclude_none=True)

        # set technology lists
        technologies = {
            "set_conversion_technologies": [
                tech.name
                for tech in self.conversion_technologies.values()
                if tech not in self.retrofitting_technologies.values()
            ],
            "set_storage_technologies": [
                tech.name for tech in self.storage_technologies.values()
            ],
            "set_transport_technologies": [
                tech.name for tech in self.transport_technologies.values()
            ],
            "set_retrofitting_technologies": [
                tech.name for tech in self.retrofitting_technologies.values()
            ],
        }

        system_json.update({k: v for k, v in technologies.items() if v})

        # Step 4: Write the dictionary to a JSON file
        with open(self.output_path / "system.json", "w") as f:
            json.dump(system_json, f, indent=4)

    # -------- Validate model ------------------------------------------------------

    def validate(self) -> None:
        """Validate the model for completeness and consistency.

        This method checks that the energy system is defined and that all
        carriers used in technologies are present in the model.
        """
        # check that all carriers of technologies are defined
        self._check_energy_system()
        self._check_carriers()

    def _check_energy_system(self) -> None:
        """
        Verifies that the energy system is complete, i.e. that all technologies
        and carriers are included in the energy system.
        """
        if self.energy_system is None:
            raise ValueError("Energy system is not defined.")

    def _check_carriers(self) -> None:
        """
        Verifies the carriers in the model.

        Checks the following:

        - each technology only has one reference carrier
        - the reference carrier of a technology is either an input or an output
          carrier
        - all carriers used in technologies are defined in the model.
        """
        # ToDo -- consider moving some of these to setters
        carriers: set[Carrier] = set()

        for technology in self.technologies.values():

            reference_carrier = (
                set(technology.reference_carrier.default_value)
                if isinstance(technology.reference_carrier.default_value, Iterable)
                else {technology.reference_carrier.default_value}
            )

            if len(reference_carrier) != 1:
                raise ValueError(
                    f"Technology {technology.name} is expected to have only "
                    f"one reference carrier, got {len(reference_carrier)}"
                )

            carriers = carriers.union(reference_carrier)

        for technology in self.conversion_technologies.values():

            input_carriers = (
                set(technology.input_carrier.default_value)
                if isinstance(technology.input_carrier.default_value, Iterable)
                else {technology.input_carrier.default_value}
            )
            output_carriers = (
                set(technology.output_carrier.default_value)
                if isinstance(technology.output_carrier.default_value, Iterable)
                else {technology.output_carrier.default_value}
            )
            reference_carrier = (
                set(technology.reference_carrier.default_value)
                if isinstance(technology.reference_carrier.default_value, Iterable)
                else {technology.reference_carrier.default_value}
            )

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
