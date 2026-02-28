from zen_creator.model import Model
from zen_creator.utils.default_config import load_config

config_path = (
    "C:\\Users\\funkec\\OneDrive - ETH Zurich\Documents\\"
    "01_Projects\\03_ZEN-garden\\00_ZEN_Creator_Raw_Data\\"
    "raw_data\\config_test.yaml"
)
existing_model_path = (
    "C:\\Users\\funkec\\Documents\\GITHUB\\01_Models\\01_ZEN_universe\\"
    "03_ZEN_data\\Test\\test_8a"
)
# Create from existing model -------------------------------------------

config = load_config(config_path)  # ToDo fix config loading
model = Model.from_existing(existing_model_path, config=config)

# Build model to set manual overwrites ---------------------------------
# model.build()

# Save model -----------------------------------------------------------
model.write()
