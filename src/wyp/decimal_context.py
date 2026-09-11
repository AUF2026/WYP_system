"""
WYP deterministic decimal context.

No binary floating-point arithmetic is used by the deterministic engine.
All quantitative operations are performed through decimal.Decimal.
"""

from __future__ import annotations

from decimal import (
    Decimal,
    InvalidOperation,
    localcontext,
)


DEFAULT_PRECISION = 120


def decimal(value: object) -> Decimal:
    """
    Convert an input into Decimal without introducing binary
    floating-point conversion.
    """
    if isinstance(value, Decimal):
        return value

    if isinstance(value, float):
        raise TypeError(
            "Binary floating-point values are forbidden. "
            "Use Decimal or a decimal string."
        )

    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise TypeError(
            f"Value cannot be represented as Decimal: {value!r}"
        ) from exc


def deterministic_context(precision: int = DEFAULT_PRECISION):
    """
    Return a local Decimal context with explicit precision.
    """
    if precision <= 0:
        raise ValueError("precision must be strictly positive")

    context = localcontext()
    context.prec = precision
    return context
