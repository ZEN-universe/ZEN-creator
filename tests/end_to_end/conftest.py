"""Pytest fixtures for end-to-end tests with registry isolation."""

from __future__ import annotations

import pytest

from zen_creator.elements import Element


@pytest.fixture(autouse=True)
def reset_element_registry():
    """Reset element registry before each test to prevent cross-test pollution.

    This function-scoped fixture restores the clean registry state before
    each test runs, ensuring that custom element classes defined in test_from_config.py
    don't interfere with tests like test_crystal_ball.
    """
    # Before the test: clear the registry to ensure no classes are registered
    Element.clear_registry()
    yield
    # After the test: do nothing
