"""
WYP deterministic engine test suite.

AUF2026 / FAURE_CORE_2026

These tests verify the executable application layer.
The formal Lean verification corpus remains a separate layer.
"""

from decimal import Decimal

import pytest

from wyp import DeterministicEngine, solve
from wyp.api import default_kernel
from wyp.kernel import UniversalKernel


def test_default_kernel_has_six_components():
    kernel = default_kernel()

    assert isinstance(kernel, UniversalKernel)

    assert kernel.component_names() == (
        "M",
        "G",
        "A",
        "Psi",
        "Lambda",
        "Proj",
    )


def test_default_kernel_contains_expected_components():
    kernel = default_kernel()

    assert kernel.M == "M"
    assert kernel.G == "G"
    assert kernel.A == "A"
    assert kernel.Psi == "Psi"
    assert kernel.Lambda == "Lambda"
    assert kernel.Proj == "Proj"


def test_kernel_tuple_has_six_components():
    kernel = default_kernel()

    assert len(kernel.as_tuple()) == 6


def test_kernel_component_lookup():
    kernel = default_kernel()

    assert kernel.component("M") == "M"
    assert kernel.component("G") == "G"
    assert kernel.component("A") == "A"
    assert kernel.component("Psi") == "Psi"
    assert kernel.component("Lambda") == "Lambda"
    assert kernel.component("Proj") == "Proj"


def test_unknown_kernel_component_is_rejected():
    kernel = default_kernel()

    with pytest.raises(KeyError):
        kernel.component("UNKNOWN")


def test_solve_returns_complete_pipeline():
    result = solve(
        {
            "x": "12",
            "y": "12",
        }
    )

    assert "structure" in result
    assert "invariants" in result
    assert "constraints" in result
    assert "quantities" in result
    assert "manifestation" in result


def test_structure_contains_six_components():
    result = solve(
        {
            "x": "12",
            "y": "12",
        }
    )

    assert result["structure"]["components"] == (
        "M",
        "G",
        "A",
        "Psi",
        "Lambda",
        "Proj",
    )


def test_representation_invariance_flag():
    result = solve(
        {
            "x": "12",
        }
    )

    assert result["invariants"]["representation_invariant"] is True


def test_structural_identity_flag():
    result = solve(
        {
            "x": "12",
        }
    )

    assert result["invariants"]["structural_identity"] is True


def test_required_component_count():
    result = solve(
        {
            "x": "12",
        }
    )

    assert result["constraints"]["required_component_count"] == 6


def test_constraints_are_valid():
    result = solve(
        {
            "x": "12",
        }
    )

    assert result["constraints"]["valid"] is True


def test_decimal_integer_string_is_exact():
    result = solve(
        {
            "x": "12",
        }
    )

    assert result["quantities"]["x"] == Decimal("12")
    assert isinstance(result["quantities"]["x"], Decimal)


def test_decimal_fixed_point_string_is_exact():
    result = solve(
        {
            "x": "12.50",
            "y": "144.000",
        }
    )

    assert result["quantities"]["x"] == Decimal("12.50")
    assert result["quantities"]["y"] == Decimal("144.000")


def test_binary_float_input_is_rejected():
    with pytest.raises(TypeError):
        solve(
            {
                "x": 12.5,
            }
        )


def test_engine_pipeline_is_deterministic():
    engine = DeterministicEngine(default_kernel())

    problem = {
        "x": "12",
        "y": "12",
    }

    result_a = engine.solve(problem)
    result_b = engine.solve(problem)

    assert result_a == result_b


def test_manifestation_status_is_deterministic():
    result = solve(
        {
            "x": "144",
        }
    )

    assert result["manifestation"]["status"] == "DETERMINISTIC"


def test_manifestation_preserves_quantities():
    result = solve(
        {
            "x": "12.50",
            "y": "144",
        }
    )

    assert result["manifestation"]["quantities"] == {
        "x": Decimal("12.50"),
        "y": Decimal("144"),
    }


def test_complete_pipeline_is_reproducible():
    problem = {
        "x": "12.50",
        "y": "144",
        "z": "660.000",
    }

    first = solve(problem)
    second = solve(problem)

    assert first == second


def test_negative_decimal_is_supported():
    result = solve(
        {
            "x": "-12.50",
        }
    )

    assert result["quantities"]["x"] == Decimal("-12.50")


def test_zero_decimal_is_supported():
    result = solve(
        {
            "x": "0",
        }
    )

    assert result["quantities"]["x"] == Decimal("0")
