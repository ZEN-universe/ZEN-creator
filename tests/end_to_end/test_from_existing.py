from pathlib import Path

from zen_creator.model import Model
from zen_creator.utils.compare_trees import compare_trees


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


if __name__ == "__main__":
    test_from_existing()
