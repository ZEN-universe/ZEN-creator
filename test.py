from zen_creator.model import Model
import zen_creator.elements.carriers.carriers as carriers
from zen_creator.elements.energy_system import EnergySystem
import zen_creator.elements.technologies.conversion_technologies as conversion_technologies
import zen_creator.sectors as sectors
from pathlib import Path
import os


source_path = "C:\\Users\\chris\\OneDrive - ETH Zurich\\Documents\\01_Projects\\03_ZEN-garden\\00_ZEN_Creator_Raw_Data\\raw_data" # TODO make configurable
config_path = Path(os.path.join(source_path, "config.yaml"))


# Create from existing model# existing_model_path = "C:\\Users\\funkec\\Documents\\GITHUB\\01_Models\\01_ZEN_universe\\03_ZEN_data\\Past_Publications\\Crystal_Ball"
# model = Model.from_existing(existing_model_path)

# Create model from scratch --------------------------------------------
model = Model("test")
model.source_path = Path(source_path)


# Create energy system -------------------------------------
model.energy_system = EnergySystem(model = model)

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
model.build() # overwrites default values

# Save model ------------------------------------------------
model.write()



