import importlib
from pathlib import Path

import tests.end_to_end.fixtures.existing_model_elements as existing_model_elements
from zen_creator.elements import (
    GenericCarrier,
    GenericConversionTechnology,
    GenericEnergySystem,
    GenericRetrofittingTechnology,
    GenericStorageTechnology,
    GenericTransportTechnology,
)
from zen_creator.model import Model
from zen_creator.utils.compare_trees import compare_trees


def _is_generic(element) -> bool:
    """Check if the element is an instance of any generic type."""
    return isinstance(
        element,
        (
            GenericCarrier,
            GenericConversionTechnology,
            GenericRetrofittingTechnology,
            GenericStorageTechnology,
            GenericTransportTechnology,
            GenericEnergySystem,
        ),
    )


def _all_types_generic(model: Model) -> None:
    """Check that all elements in the model are generic types.

    This is used to verify that no custom element classes were registered
    when loading from an existing model without a config. Raises an AssertionError
    if any non-generic types are found.
    """
    for element in model.elements.values():
        if not _is_generic(element):
            raise AssertionError(
                f"Expected generic Element, got {element.__class__.__name__}"
            )

    # Check that the energy system is a generic type
    if not _is_generic(model.energy_system):
        raise AssertionError(
            "Expected generic EnergySystem, got "
            f"{model.energy_system.__class__.__name__}"
        )


def _no_types_generic(model: Model) -> None:
    """Check that no elements in the model are generic types.

    This is used to verify that all custom element classes were registered
    when loading from an existing model with a config. Raises an AssertionError
    if any generic types are found.
    """
    for element in model.elements.values():
        if _is_generic(element):
            raise AssertionError(
                "Expected non-generic Element, got " f"{element.__class__.__name__}"
            )

    # Check that the energy system is a non-generic type
    if _is_generic(model.energy_system):
        raise AssertionError(
            "Expected non-generic EnergySystem, got "
            f"{model.energy_system.__class__.__name__}"
        )


def test_crystal_ball():
    """
    Test the Model.from_existing() constructor without a config.

    This test:
        1. Loads an existing model into a model object using the
           ``Model.from_existing()`` constructor.
        2. Writes the model to a new output folder.
        3. Verifies that the original model and the new model are
           identical.

    The current test case matches ``test_8a`` in ZEN-garden.
    """

    # set file paths
    existing_model_path = Path(".//tests//end_to_end//fixtures//crystal_ball")

    # create and save model
    model = Model.from_existing(existing_model_path=existing_model_path)

    # save under new name
    model.output_folder = Path(".//tests//end_to_end//outputs")
    model.name = "test_crystal_ball"

    # build should do nothing
    model.build()

    # write model to new output folder
    model.write()

    # Verify that the new model matches the existing model path
    # Compares file trees and files
    compare_trees(existing_model_path, model.output_path, raise_error=True)

    # Check that all elements are generic types (i.e. no custom classes were registered)
    _all_types_generic(model)


def test_from_existing():
    """
    Test the Model.from_existing() constructor without a config.

    This test:
        1. Loads an existing model into a model object using the
           ``Model.from_existing()`` constructor.
        2. Writes the model to a new output folder.
        3. Verifies that the original model and the new model are
           identical.

    The current test case matches ``test_8a`` in ZEN-garden.
    """

    # set file paths
    existing_model_path = Path(".//tests//end_to_end//fixtures//existing_model")

    # create and save model
    model = Model.from_existing(existing_model_path=existing_model_path)
    model.output_folder = Path(".//tests//end_to_end//outputs")
    model.name = "test_from_existing"
    model.write()

    # Verify that the new model matches the existing model path
    # Compares file trees and files
    compare_trees(existing_model_path, model.output_path, raise_error=True)

    # check that no types are generic (i.e. all custom classes were registered)
    _all_types_generic(model)


def test_from_existing_with_config():
    """
    Test the Model.from_existing() constructor.

    This test:
        1. Loads an existing model into a model object using the
           ``Model.from_existing()`` constructor with a config file.
        2. Writes the model to a new output folder.
        3. Verifies that the original model and the new model are
           identical.

    The current test case matches ``test_8a`` in ZEN-garden.
    """
    # import element classes locally to avoid global registry contamination
    # importing custom element classes registers them in the Element registry,
    # This allows the elements to be assigned to the custom classes upon
    # model creation.
    importlib.reload(existing_model_elements)

    # set file paths
    existing_model_path = Path(".//tests//end_to_end//fixtures//existing_model")
    config = Path(".//tests//end_to_end//fixtures//config_existing_model.yaml")

    # create and save model
    model = Model.from_existing(existing_model_path=existing_model_path, config=config)
    model.output_folder = Path(".//tests//end_to_end//outputs")
    model.write()

    # Verify that the new model matches the existing model path
    # Compares file trees and files
    compare_trees(existing_model_path, model.output_path, raise_error=True)

    # check that no types are generic (i.e. all custom classes were registered)
    _no_types_generic(model)
