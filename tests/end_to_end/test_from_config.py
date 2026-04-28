"""Test for creating models from config using custom element classes.

Element classes are imported locally within the test function to avoid
registering them globally, which would cause contamination of other tests.
"""

from __future__ import annotations

import importlib
from pathlib import Path

import tests.end_to_end.fixtures.existing_model_elements as existing_model_elements
from zen_creator.model import Model
from zen_creator.utils.compare_trees import compare_trees
from zen_creator.utils.default_config import Config

FIXTURE_ROOT = Path(__file__).parent / "fixtures"
EXISTING_MODEL_PATH = FIXTURE_ROOT / "existing_model"
CONFIG_PATH = FIXTURE_ROOT / "config_existing_model.yaml"
OUTPUT_FOLDER = Path(".//tests//end_to_end//outputs")


def test_from_config():
    """Recreate the existing_model fixture tree from config and explicit classes.

    Note: Element classes are imported locally to prevent global registry
    contamination when this test runs alongside other tests.
    """
    importlib.reload(existing_model_elements)

    config = Config.load_from_yaml(CONFIG_PATH)
    config.source_path = str(EXISTING_MODEL_PATH)

    model = Model.from_config(config)
    model.output_folder = OUTPUT_FOLDER
    model.name = "test_from_config_existing_model_replica"
    model.build()
    model.write()

    compare_trees(EXISTING_MODEL_PATH, model.output_path, raise_error=True)


def test_from_config_str():
    """Recreate the existing_model fixture tree from config and explicit classes.

    Calls the config file via a string path instead of a Config object.

    Note: Element classes are imported locally to prevent global registry
    contamination when this test runs alongside other tests.
    """
    importlib.reload(existing_model_elements)

    model = Model.from_config(CONFIG_PATH)
    model.output_folder = OUTPUT_FOLDER
    model.name = "test_from_config_str_existing_model_replica"
    model.build()
    model.write()

    compare_trees(EXISTING_MODEL_PATH, model.output_path, raise_error=True)
