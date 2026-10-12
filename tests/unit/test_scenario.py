"""Unit tests for the scenario analysis."""

from __future__ import annotations

import pandas as pd
import pytest
import yaml

from zen_creator.datasets.datasets.metadata import AssumptionInformation
from zen_creator.elements.carriers.aa_template import TemplateCarrier
from zen_creator.model import Model
from zen_creator.utils.scenario import Scenario, ValueList


def _source() -> AssumptionInformation:
    """Return a minimal source for set_data calls."""
    return AssumptionInformation(description="Scenario test assumption.")


def _demand_df() -> pd.DataFrame:
    """Return a small time series usable as demand data."""
    return pd.DataFrame({"demand": [1.0, 2.0]}, index=pd.Index([0, 1], name="time"))


# ---------- Scenario ----------


def test_scenario_requires_an_entry_type():
    """A scenario without any change is rejected."""
    with pytest.raises(ValueError, match="does not change anything"):
        Scenario("empty")


def test_scenario_rejects_unit_without_default_value():
    """A unit is only meaningful together with a default value."""
    with pytest.raises(ValueError, match="sets a unit"):
        Scenario("cheap", unit="Euro/MWh", default_op=2.0)


def test_scenario_rejects_format_without_placeholder():
    """A format without a placeholder cannot name sub-scenarios."""
    with pytest.raises(ValueError, match="placeholder"):
        Scenario("value_list", default_op=[1.0, 2.0], fmt="value_list")


def test_scenario_entry_of_default_value():
    """A default value points to the attributes file of the scenario."""
    scenario = Scenario("cheap", default_value=1.5)

    assert scenario.entries("price_import") == {
        "price_import": {"default": "attributes_cheap"}
    }


def test_scenario_entry_of_data():
    """Data points to a csv file and yearly variations to their own parameter."""
    scenario = Scenario("nodal", df=_demand_df(), yearly_variations_df=_demand_df())

    assert scenario.entries("demand") == {
        "demand": {"file": "demand_nodal"},
        "demand_yearly_variation": {"file": "demand_yearly_variation_nodal"},
    }


def test_scenario_entry_of_operators():
    """Scalar operators are written as they are."""
    scenario = Scenario("scaled", default_op=1.5, file_op=0.5)

    assert scenario.entries("demand") == {"demand": {"default_op": 1.5, "file_op": 0.5}}


def test_scenario_entry_of_list_operator():
    """A list operator gets a format so that sub-scenarios are named."""
    scenario = Scenario("value_list", default_op=[0.5, 1.5])

    assert scenario.entries("demand") == {
        "demand": {"default_op": [0.5, 1.5], "default_op_fmt": "demand_{}"}
    }


def test_scenario_entry_of_two_list_operators():
    """Two expanded operators get formats that are distinguishable."""
    scenario = Scenario("value_list", default_op=[0.5], file_op=[1.5])

    assert scenario.entries("demand") == {
        "demand": {
            "default_op": [0.5],
            "default_op_fmt": "demand_default_op_{}",
            "file_op": [1.5],
            "file_op_fmt": "demand_file_op_{}",
        }
    }


def test_scenario_rejects_non_numeric_operator():
    """Operators must be numeric, since ZEN-garden multiplies with them."""
    scenario = Scenario("broken", default_op="high")

    with pytest.raises(ValueError, match="must be numeric"):
        scenario.entries("demand")


def test_scenario_uses_explicit_suffix():
    """An explicit suffix replaces the scenario name in the file names."""
    scenario = Scenario("cheap", default_value=1.5, suffix="low")

    assert scenario.entries("demand") == {"demand": {"default": "attributes_low"}}


# ---------- Registration ----------


def test_set_data_registers_scenarios(model: Model):
    """scenarios passed to set_data end up in the registry of the model."""
    carrier = TemplateCarrier(model=model)
    carrier.build()

    carrier.demand.set_data(
        source=_source(),
        default_value=2.0,
        scenarios=Scenario("cheap", default_value=1.0),
    )

    assert model.scenarios.names == ["cheap"]
    assert model.scenarios.to_dict() == {
        "cheap": {"template_carrier": {"demand": {"default": "attributes_cheap"}}}
    }


def test_duplicate_scenario_on_attribute_is_rejected(model: Model):
    """The same scenario cannot be attached twice to one attribute."""
    carrier = TemplateCarrier(model=model)
    carrier.build()

    carrier.demand.add_scenarios(Scenario("cheap", default_op=0.5))

    with pytest.raises(ValueError, match="already defined for attribute"):
        carrier.demand.add_scenarios(Scenario("cheap", default_op=0.6))


def test_scenario_default_value_reuses_attribute_validation(model: Model):
    """A scenario's default value must be valid for the attribute, like the base."""
    carrier = TemplateCarrier(model=model)
    carrier.build()

    with pytest.raises(ValueError, match="must be a float, int, or list"):
        carrier.demand.add_scenarios(
            Scenario("broken", default_value="high")  # type: ignore[arg-type]
        )


def test_scenario_df_reuses_attribute_index_validation(model: Model):
    """A scenario's data must use index names the attribute allows, like the base."""
    carrier = TemplateCarrier(model=model)
    carrier.build()

    bad_df = pd.DataFrame({"demand": [1.0]}, index=pd.Index([0], name="not_allowed"))

    with pytest.raises(ValueError, match="Invalid index names"):
        carrier.demand.add_scenarios(Scenario("nodal", df=bad_df))


def test_scenario_list_default_value_reuses_list_validation(model: Model):
    """A scenario's list default value must be allowed for the attribute."""
    carrier = TemplateCarrier(model=model)
    carrier.build()

    # 'demand' does not support list default values, only e.g. conversion_factor
    with pytest.raises(ValueError, match="does not support a list"):
        carrier.demand.add_scenarios(Scenario("broken", default_value=[1.0]))


def test_energy_system_uses_its_own_key(model: Model):
    """The energy system is addressed as 'EnergySystem' in scenarios.yaml."""
    from zen_creator.elements import GenericEnergySystem

    energy_system = GenericEnergySystem(model=model)

    assert energy_system.scenario_key == "EnergySystem"


# ---------- Writing ----------


def test_write_creates_scenario_files(model: Model):
    """scenarios with data are written next to the files of the default run."""
    carrier = TemplateCarrier(model=model)
    carrier.build()

    carrier.demand.set_data(
        source=_source(),
        default_value=2.0,
        unit="MW",
        scenarios=[
            Scenario("cheap", default_value=1.0, unit="GW"),
            Scenario("nodal", df=_demand_df()),
        ],
    )
    carrier.write()

    out_path = carrier.output_path
    assert (out_path / "demand_nodal.csv").exists()

    with (out_path / "attributes_cheap.yaml").open() as f:
        attributes = yaml.safe_load(f)

    assert attributes["demand"] == {"default_value": 1.0, "unit": "GW"}
    # the remaining attributes keep their default values
    assert attributes["price_shed_demand"] == {
        "default_value": "inf",
        "unit": "Euro/MWh",
    }


def test_write_merges_attributes_of_one_scenario(model: Model):
    """Several attributes of one scenario share a single attributes file."""
    carrier = TemplateCarrier(model=model)
    carrier.build()

    carrier.demand.add_scenarios(Scenario("cheap", default_value=1.0))
    carrier.price_shed_demand.add_scenarios(Scenario("cheap", default_value=2.0))
    carrier.write()

    with (carrier.output_path / "attributes_cheap.yaml").open() as f:
        attributes = yaml.safe_load(f)

    assert attributes["demand"]["default_value"] == 1.0
    assert attributes["price_shed_demand"]["default_value"] == 2.0


def test_write_model_creates_scenario_file(model: Model, tmp_path):
    """The model writes scenarios.yaml and turns on the scenario analysis."""
    from zen_creator.elements import GenericEnergySystem

    model.energy_system = GenericEnergySystem(model=model)
    model.config.system.set_nodes = ["CH"]
    model.build()

    model.scenarios.add("coarse", system={"set_nodes": ["DE"]})
    model.write()

    with (model.output_path / "system.yaml").open() as f:
        system = yaml.safe_load(f)
    with (model.output_path / "scenarios.yaml").open() as f:
        scenarios = yaml.safe_load(f)

    assert system["conduct_scenario_analysis"] is True
    assert scenarios == {"coarse": {"system": {"set_nodes": ["DE"]}}}


# ---------- Configuration overrides ----------


def test_add_rejects_wrong_setting_type(model: Model):
    """A system override has to keep the type of the setting."""
    model.config.system.aggregated_time_steps_per_year = 96

    with pytest.raises(ValueError, match="but it is of type"):
        model.scenarios.add("coarse", system={"aggregated_time_steps_per_year": "96"})


def test_add_expands_a_value_list(model: Model):
    """A value_list is written as the expansion entry of ZEN-garden."""
    model.config.system.aggregated_time_steps_per_year = 96

    model.scenarios.add(
        "resolution", system={"aggregated_time_steps_per_year": ValueList([24, 96])}
    )

    assert model.scenarios.to_dict() == {
        "resolution": {
            "system": {
                "aggregated_time_steps_per_year": {
                    "value": [24, 96],
                    "value_fmt": "aggregated_time_steps_per_year_{}",
                }
            }
        }
    }


def test_scenarios_from_config():
    """Scenarios declared in the configuration file reach the registry."""
    from zen_creator.utils.config import Config

    config = Config(
        system={
            "set_nodes": ["CH"],
            "reference_year": 2020,
            "optimized_years": 2,
            "interval_between_years": 1,
        },
        scenarios={"coarse": {"system": {"reference_year": {"values": [2030, 2040]}}}},
    )

    model = Model.from_config(config)

    assert model.scenarios.to_dict() == {
        "coarse": {
            "system": {
                "reference_year": {
                    "value": [2030, 2040],
                    "value_fmt": "reference_year_{}",
                }
            }
        }
    }


def test_config_scenario_rejects_unknown_block():
    """Only settings can be varied through the configuration file."""
    from zen_creator.utils.config import Config

    config = Config(
        system={
            "set_nodes": ["CH"],
            "reference_year": 2020,
            "optimized_years": 2,
            "interval_between_years": 1,
        },
        scenarios={"broken": {"natural_gas": {"price_import": {"default_op": 2}}}},
    )

    with pytest.raises(ValueError, match="Only system, analysis, solver"):
        Model.from_config(config)


# ---------- Set-wide entries ----------


def test_add_set_entry(model: Model):
    """A set entry addresses every element of the set."""
    model.scenarios.add_set(
        "slow",
        "set_technologies",
        "max_diffusion_rate",
        default_op=0.5,
        exclude=["photovoltaics"],
    )

    assert model.scenarios.to_dict() == {
        "slow": {
            "set_technologies": {
                "max_diffusion_rate": {"default_op": 0.5, "exclude": ["photovoltaics"]}
            }
        }
    }


def test_add_set_rejects_unknown_set(model: Model):
    """Only the element sets of ZEN-garden can be addressed."""
    with pytest.raises(ValueError, match="Unknown set"):
        model.scenarios.add_set("slow", "set_things", "lifetime", default_op=0.5)


def test_duplicate_parameter_in_scenario_is_rejected(model: Model):
    """The same parameter cannot be set twice in one scenario."""
    model.scenarios.add_set("slow", "set_technologies", "lifetime", default_op=0.5)

    with pytest.raises(ValueError, match="already defined in scenario"):
        model.scenarios.add_set("slow", "set_technologies", "lifetime", default_op=2.0)


def test_validate_rejects_unknown_element(model: Model):
    """Scenarios must refer to elements that are part of the model."""
    model.scenarios._register("odd", "unknown_carrier", "demand", {"default_op": 2.0})

    with pytest.raises(ValueError, match="not"):
        model.scenarios.validate()


# ---------- Global scenario definitions ----------


def test_apply_global_scenarios_allows_settings_and_sets(model: Model):
    """Settings overrides and set-wide entries are allowed in the global scope."""

    def define_global_scenarios(m: Model) -> None:
        m.scenarios.add("coarse", system={"set_nodes": ["DE"]})
        m.scenarios.add_set(
            "slow", "set_technologies", "max_diffusion_rate", default_op=0.5
        )

    model.apply_global_scenarios(define_global_scenarios)

    assert set(model.scenarios.names) == {"coarse", "slow"}


def test_apply_global_scenarios_rejects_element_level_scenario(model: Model):
    """Element-level scenarios must be defined where the attribute is set."""
    carrier = TemplateCarrier(model=model)
    carrier.build()

    def define_global_scenarios(m: Model) -> None:
        carrier.demand.add_scenarios(Scenario("cheap", default_op=0.5))

    with pytest.raises(ValueError, match="global scenario definitions"):
        model.apply_global_scenarios(define_global_scenarios)


def test_global_scope_is_released_after_an_error(model: Model):
    """A failed global definition does not leave the registry locked."""
    carrier = TemplateCarrier(model=model)
    carrier.build()

    def broken(m: Model) -> None:
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        model.apply_global_scenarios(broken)

    # registering an element-level scenario works again afterwards
    carrier.demand.add_scenarios(Scenario("cheap", default_op=0.5))
    assert model.scenarios.names == ["cheap"]


if __name__ == "__main__":
    pytest.main([__file__])
