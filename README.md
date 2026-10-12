# ZEN-creator

Lightweight utilities for creating and managing ZEN energy-system models and
associated datasets. Full developer and user documentation is available online.

## Quick start

### Installation (recommended)

- Create the conda environment included with the repository:

```bash
conda env create -f zen_creator_env.yml
conda activate zen-creator-env
```

- Or install in editable mode with pip:

```bash
python -m pip install -e .
```

### Basic usage

Programmatic usage is the recommended way to build and manipulate ZEN
models. The central entry point is the `Model` class which can be constructed
in several ways: directly, from a configuration file, or by loading an
existing ZEN-garden input folder.

```python
from pathlib import Path
from zen_creator.model import Model

# 1) Create a model from a configuration file
model = Model.from_config(Path("config.yaml"))
model.build()
model.validate()
model.write()

# 2) Load an existing ZEN-garden input folder and update
existing = Path("existing_model")
model2 = Model.from_existing(existing)
model2.name = "updated_model"
model2.build()
model2.write()

# 3) Create an empty model and add sectors/elements programmatically
m = Model()
m.add_sector_by_name("electricity")
m.add_element_by_name("electricity", generic="carrier")
m.build()
```


### Settings, variants and scenarios

- Projects define typed settings as `SettingsCategory` subclasses, set in the
  `settings:` block of the configuration file and available as
  `model.settings.<category>.<field>`.
- A models file declares named variants of a dataset as sparse patches of the
  settings, read with `ModelSet`.
- Scenarios for ZEN-garden's scenario analysis are attached to attributes via
  `Attribute.set_data(scenarios=...)` or added with `model.scenarios.add()` and
  `model.scenarios.add_set()`, and written to `scenarios.yaml`.

### Useful properties

- `model.carriers`, `model.technologies`: dictionaries of elements
- `model.output_path`: path where the model will be written

## Documentation

The full documentation (API reference, developer guide and examples) is hosted
online: [ZEN-creator documentation](https://zen-creator.readthedocs.io/en/latest/)

## Contributing

project [Contribution Guide](https://zen-creator.readthedocs.io/en/latest/files/developer_guide/contributing.html).
