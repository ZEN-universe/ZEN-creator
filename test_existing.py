from zen_creator.model import Model
import zen_creator.elements.carriers.carriers as carriers
import zen_creator.elements.technologies.conversion_technologies as conversion_technologies
import zen_creator.sectors as sectors
from pathlib import Path
from zen_creator.utils.attribute import Attribute
import os

from zen_creator.utils.default_config import load_config


source_path = "C:\\Users\\jmannhardt\\Desktop\\02-ZEN\\ZEN-creator\\raw_data" # TODO make configurable
config_path = Path(os.path.join(source_path, "config.yaml"))


# Create from existing model -------------------------------------------
existing_model_path = "C:\\Users\\jmannhardt\\Desktop\\02-ZEN\\data\\Crystal_Ball"
config = load_config(config_path)['model_1'] #ToDo fix config loading
config.main_settings.source_path = source_path # ToDo make source path configurable
model = Model.from_existing(
     existing_model_path, config=config
)

# Build model to set manual overwrites ---------------------------------
model.build()

# Save model -----------------------------------------------------------
model.write()



