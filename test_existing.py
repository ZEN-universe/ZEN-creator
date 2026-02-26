import os
from pathlib import Path

from zen_creator.model import Model
from zen_creator.utils.default_config import load_config

source_path = (
    "C:\\Users\\funkec\\OneDrive - ETH Zurich\Documents\\"
    "01_Projects\\03_ZEN-garden\\00_ZEN_Creator_Raw_Data\\"
    "raw_data"
)  # TODO make configurable
config_path = Path(os.path.join(source_path, "config_test.yaml"))


# Create from existing model -------------------------------------------
existing_model_path = (
    "C:\\Users\\funkec\\Documents\\GITHUB\\01_Models\\01_ZEN_universe\\"
    "03_ZEN_data\\Test\\test_8a"
)
config = load_config(config_path)["model_1"]  # ToDo fix config loading
model = Model.from_existing(existing_model_path, config=config)

# Build model to set manual overwrites ---------------------------------
# model.build()

# Save model -----------------------------------------------------------
model.write()
