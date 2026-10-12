"""Guard against drift between ZEN-creator's config mirror and ZEN-garden.

ZEN-creator does not depend on ZEN-garden, so ``AnalysisConfig``,
``SolverConfig`` and ``SystemConfig`` restate ZEN-garden's fields and
defaults. These tests compare them against ZEN-garden itself whenever it is
importable, and skip otherwise.
"""

from __future__ import annotations

import pytest

from zen_creator.utils.config import (
    AnalysisConfig,
    HeaderDataInputsConfig,
    SolverConfig,
    SubsetsConfig,
    SystemConfig,
    TimeSeriesAggregationConfig,
)

zen_garden_config = pytest.importorskip(
    "zen_garden.config", reason="ZEN-garden is not installed"
)

MIRRORED_CLASSES = [
    (SystemConfig, "System"),
    (AnalysisConfig, "Analysis"),
    (SolverConfig, "Solver"),
    (SubsetsConfig, "Subsets"),
    (HeaderDataInputsConfig, "HeaderDataInputs"),
    (TimeSeriesAggregationConfig, "TimeSeriesAggregation"),
]


@pytest.mark.parametrize("mirror, zen_garden_name", MIRRORED_CLASSES)
def test_mirror_has_the_same_fields(mirror, zen_garden_name: str) -> None:
    """The mirror declares exactly the fields ZEN-garden declares."""
    original = getattr(zen_garden_config, zen_garden_name)

    assert set(mirror.model_fields) == set(original.model_fields)


@pytest.mark.parametrize("mirror, zen_garden_name", MIRRORED_CLASSES)
def test_mirror_has_the_same_defaults(mirror, zen_garden_name: str) -> None:
    """The mirror uses the same defaults as ZEN-garden.

    Nested config blocks are compared as dictionaries, since the mirror and
    ZEN-garden use different classes for them.
    """
    original = getattr(zen_garden_config, zen_garden_name)

    assert mirror().model_dump() == original().model_dump()
