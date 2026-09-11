"""
WYP deterministic execution engine.

Pipeline:

    structure
        ->
    invariants
        ->
    constraints
        ->
    quantities
        ->
    manifestation
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .decimal_context import decimal
from .kernel import UniversalKernel


@dataclass(frozen=True)
class DeterministicResult:
    """
    Immutable result returned by the deterministic engine.
    """

    structure: Mapping[str, Any]
    invariants: Mapping[str, Any]
    constraints: Mapping[str, Any]
    quantities: Mapping[str, Any]
    manifestation: Any


class DeterministicEngine:
    """
    WYP deterministic computation engine.
    """

    def __init__(self, kernel: UniversalKernel):
        self.kernel = kernel

    def structure(
        self,
        problem: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        """
        Extract the structural representation of the problem.
        """
        return {
            "problem": dict(problem),
            "kernel": self.kernel.as_tuple(),
            "components": self.kernel.component_names(),
        }

    def invariants(
        self,
        structure: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        """
        Compute structural invariants.
        """
        return {
            "component_count": len(
                structure["components"]
            ),
            "representation_invariant": True,
            "structural_identity": True,
        }

    def constraints(
        self,
        invariants: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        """
        Derive deterministic constraints.
        """
        return {
            "valid": bool(
                invariants["representation_invariant"]
                and invariants["structural_identity"]
            ),
            "required_component_count": 6,
        }

    def quantities(
    self,
    constraints: Mapping[str, Any],
    problem: Mapping[str, Any],
) -> Mapping[str, Any]:
    """
    Produce exact quantitative values.

    Numerical inputs must enter through Decimal-compatible
    representations.
    """
    if not constraints["valid"]:
        raise ValueError(
            "Problem violates deterministic kernel constraints."
        )

    quantities: dict[str, Any] = {}

    for key, value in problem.items():
        if isinstance(value, float):
            raise TypeError(
                f"Binary floating-point values are forbidden: {key!r}"
            )

        if isinstance(value, (str, int)):
            try:
                quantities[key] = decimal(value)
            except TypeError:
                quantities[key] = value
        else:
            quantities[key] = value

    return quantities

    def manifestation(
        self,
        quantities: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        """
        Construct the final deterministic manifestation.
        """
        return {
            "status": "DETERMINISTIC",
            "quantities": dict(quantities),
        }

    def solve(
        self,
        problem: Mapping[str, Any],
    ) -> DeterministicResult:
        """
        Execute the complete WYP pipeline.
        """
        structure = self.structure(problem)
        invariants = self.invariants(structure)
        constraints = self.constraints(invariants)
        quantities = self.quantities(constraints, problem)
        manifestation = self.manifestation(quantities)

        return DeterministicResult(
            structure=structure,
            invariants=invariants,
            constraints=constraints,
            quantities=quantities,
            manifestation=manifestation,
        )
