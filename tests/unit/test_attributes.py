"""Unit tests for Attribute methods."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from zen_creator import Model
from zen_creator.elements import Element


class MockElement(Element):
    """Mock Element class for testing."""

    name = "mock_element"
    power_unit = "MW"


def test_attribute_construction() -> None:
    """Test that an Attribute can be constructed with valid parameters."""
    from zen_creator.attributes.attribute import Attribute

    model = Model()
    element = MockElement(model)  # Replace with a mock or actual element if needed
    attr = Attribute(
        name="input_carrier",
        element=element,
        default_value=10.0,
        unit="MW",
    )

    assert attr.name == "input_carrier"
    assert attr.default_value == 10.0
    assert attr.unit == "MW"


def test_attribute_min_max_validation() -> None:
    """Test that the min/max validation works correctly."""
    from zen_creator.attributes.attribute import Attribute

    model = Model()
    element = MockElement(model)
    attr = Attribute(
        name="input_carrier",
        element=element,
        default_value=10.0,
        unit="MW",
        minimum_value=0.0,
        maximum_value=100.0,
    )

    # Valid values
    attr.default_value = 50
    attr.default_value = 50.0
    attr.default_value = [10.0, 20.0, 30.0]
    attr.df = pd.DataFrame(
        {"value": [10.0, 20.0, 30.0]}, index=pd.Index(["A", "B", "C"], name="node")
    )
    attr.year_specific_dfs = {
        2020: pd.DataFrame(
            {"value": [10.0, 20.0, 30.0]}, index=pd.Index(["A", "B", "C"], name="node")
        ),
        2021: pd.DataFrame(
            {"value": [15.0, 25.0, 35.0]}, index=pd.Index(["A", "B", "C"], name="node")
        ),
    }
    attr.year_specific_dfs = {}
    attr.yearly_variations_df = pd.DataFrame(
        {"value": [10.0, 20.0, 30.0]}, index=pd.Index(["A", "B", "C"], name="node")
    )
    attr.yearly_variations_df = None

    # Invalid values
    with pytest.raises(ValueError):
        attr.default_value = -10.0
    with pytest.raises(ValueError):
        attr.default_value = np.inf
    with pytest.raises(ValueError):
        attr.default_value = [10.0, 200.0, 30.0]
    with pytest.raises(ValueError):
        attr.df = pd.DataFrame({"value": [-10.0, 20.0, 30.0]})
    with pytest.raises(ValueError):
        attr.year_specific_dfs = {
            2020: pd.DataFrame({"value": [10.0, -20.0, 30.0]}),
            2021: pd.DataFrame({"value": [15.0, 25.0, 35.0]}),
        }
    with pytest.raises(ValueError):
        attr.yearly_variations_df = pd.DataFrame({"value": [10.0, -20.0, 30.0]})
