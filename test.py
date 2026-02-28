import os
from pathlib import Path

import zen_creator.sectors as sectors
from zen_creator.elements import conversion_technologies as conversion_technologies
from zen_creator.elements.energy_system import EnergySystem
from zen_creator.model import Model
from zen_creator.utils.default_config import load_config

source_path = (
    "C:\\Users\\funkec\\OneDrive - ETH Zurich\Documents\\"
    "01_Projects\\03_ZEN-garden\\00_ZEN_Creator_Raw_Data\\"
    "raw_data"
)  # TODO make configurable
config_path = Path(os.path.join(source_path, "config.yaml"))
config = load_config(config_path)["model_1"]  # ToDo fix config loading

# Create model from scratch --------------------------------------------
model = Model(config)
model.source_path = Path(source_path)


# Create energy system -------------------------------------
model.energy_system = EnergySystem(model=model)

# Add whole sector to the model -----------------------------
model.add_sector(sectors.Electricity)

# Remove whole sector from model -----------------------------
model.remove_sector(sectors.Electricity)


# Add elements to model individually -----------------------
# Adding elements only initializes the classes and sets default values.
model.add_element(conversion_technologies.ElectrodeBoiler)
model.add_element(conversion_technologies.HeatPump)
model.add_element(conversion_technologies.Photovoltaics)


# These elements do not work yet ---------------------------
# model.add_element(conversion_technologies.LigniteCoalPlant)
# model.add_element(carriers.Lignite)
# model.add_element(carriers.Electricity)
# model.add_element(carriers.Heat)

# Remove element from the model ----------------------------
model.remove_element(conversion_technologies.ElectrodeBoiler)


# Build model using user-defined data -----------------------
model.build()  # overwrites default values

# Save model ------------------------------------------------
model.write()
