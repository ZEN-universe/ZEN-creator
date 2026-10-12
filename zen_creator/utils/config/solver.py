"""Mirror of the ``solver`` block of ZEN-garden's config file.

The fields and defaults mirror ``zen_garden.config``. ZEN-creator does not
depend on ZEN-garden, so the mirror is kept in sync by
``tests/unit/test_zen_garden_schema.py``, which compares the field sets
whenever ZEN-garden is importable.
"""

from typing import Any, Union

from pydantic import Field

from ._base import Subscriptable


class SolverConfig(Subscriptable):
    """Config for the solver, e.g. its name, options and scaling."""

    name: str = "highs"
    solver_options: dict[str, Any] = Field(default_factory=dict)
    check_unit_consistency: bool = True
    solver_dir: str = ".//outputs//solver_files"
    keep_files: bool = False
    io_api: str = "lp"
    save_duals: bool = False
    save_reduced_costs: bool = False
    save_parameters: bool = True
    # empty lists mean that everything is saved
    selected_saved_parameters: list[str] = Field(default_factory=list)
    selected_saved_variables: list[str] = Field(default_factory=list)
    selected_saved_duals: list[str] = Field(default_factory=list)
    selected_saved_reduced_costs: list[str] = Field(default_factory=list)
    round_parameters: bool = False
    rounding_decimal_points_units: int = 6
    rounding_decimal_points_capacity: int = 4
    rounding_decimal_points_tsa: int = 4
    analyze_numerics: bool = True
    run_diagnostics: bool = False
    use_scaling: bool = True
    scaling_include_rhs: bool = True
    scaling_algorithm: Union[list[str], str] = Field(
        default_factory=lambda: ["geom", "geom", "geom"]
    )
