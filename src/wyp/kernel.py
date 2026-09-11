"""
WYP deterministic kernel.

Application-level representation of the six-component universal kernel:

    U_F = (M, G, A, Psi, Lambda, Proj)

The implementation is deliberately independent from the formal Lean
verification corpus. Lean remains the formal verification layer;
this module is the executable application layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping


@dataclass(frozen=True)
class UniversalKernel:
    """
    Executable representation of the six-component kernel.
    """

    M: Any
    G: Any
    A: Any
    Psi: Any
    Lambda: Any
    Proj: Any

    def as_tuple(self) -> tuple[Any, Any, Any, Any, Any, Any]:
        return (
            self.M,
            self.G,
            self.A,
            self.Psi,
            self.Lambda,
            self.Proj,
        )

    def component_names(self) -> tuple[str, ...]:
        return (
            "M",
            "G",
            "A",
            "Psi",
            "Lambda",
            "Proj",
        )

    def component(self, name: str) -> Any:
        components: Mapping[str, Any] = {
            "M": self.M,
            "G": self.G,
            "A": self.A,
            "Psi": self.Psi,
            "Lambda": self.Lambda,
            "Proj": self.Proj,
        }

        try:
            return components[name]
        except KeyError as exc:
            raise KeyError(
                f"Unknown kernel component: {name!r}"
            ) from exc

    def map_components(
        self,
        transform: Callable[[Any], Any],
    ) -> "UniversalKernel":
        """
        Apply the same structural transformation to every component.
        """
        return UniversalKernel(
            M=transform(self.M),
            G=transform(self.G),
            A=transform(self.A),
            Psi=transform(self.Psi),
            Lambda=transform(self.Lambda),
            Proj=transform(self.Proj),
        )
