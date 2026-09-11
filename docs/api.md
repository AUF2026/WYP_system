````
# WYP System — API Reference

## 1. Overview

The WYP public API provides a programmatic interface to the deterministic
execution engine.

The primary entry point is:

```python
from wyp import solve
````

 The API is intentionally small. Application code submits a problem\
 representation and receives the complete WYP execution result.

---

 ## 2\. Public Interface

 The package publicly exposes:

```
from wyp import DeterministicEngine
from wyp import solve
```

 The public package interface is defined by:

```
__all__ = [
    "DeterministicEngine",
    "solve",
]
```

---

 ## 3\. `solve()`

 ### Signature

```
solve(problem: Mapping[str, Any]) -> dict[str, Any]
```

 ### Description

 `solve()` is the principal high-level WYP execution function.

 It constructs the default six-component kernel, initializes the\
 deterministic engine, executes the complete processing pipeline, and\
 returns the resulting data structure.

 ### Example

```
from wyp import solve

result = solve(
    {
        "x": "12",
        "y": "12",
    }
)

print(result)
```

---

 ## 4\. Result Structure

 The result returned by `solve()` contains five principal fields:

```
structure
invariants
constraints
quantities
manifestation
```

 Conceptually:

```
problem
   ↓
structure
   ↓
invariants
   ↓
constraints
   ↓
quantities
   ↓
manifestation
```

---

 ## 5\. `structure`

 The `structure` field contains the structural representation of the\
 submitted problem.

 Example:

```
result["structure"]
```

 The structure includes:

```
problem
kernel
components
```

 The `components` field identifies the six kernel components:

```
(
    "M",
    "G",
    "A",
    "Psi",
    "Lambda",
    "Proj",
)
```

---

 ## 6\. `invariants`

 The `invariants` field contains the structural properties evaluated by\
 the engine.

 The current implementation exposes:

```
component_count
representation_invariant
structural_identity
```

 Example:

```
result["invariants"]["representation_invariant"]
```

 returns:

```
True
```

 for a valid default kernel execution.

---

 ## 7\. `constraints`

 The `constraints` field contains the conditions derived from the\
 invariants.

 The current implementation exposes:

```
valid
required_component_count
```

 Example:

```
result["constraints"]["valid"]
```

 A valid six-component kernel produces:

```
True
```

---

 ## 8\. `quantities`

 The `quantities` field contains the numerical values accepted and\
 processed by the quantitative layer.

 Decimal values are represented by:

```
decimal.Decimal
```

 Example:

```
result = solve(
    {
        "x": "12.50",
    }
)

print(result["quantities"]["x"])
```

 The resulting value is:

```
Decimal("12.50")
```

---

 ## 9\. Decimal Input Policy

 The WYP quantitative layer does not accept binary floating-point\
 values.

 This input is valid:

```
{
    "x": "12.50"
}
```

 This input is also valid:

```
{
    "x": Decimal("12.50")
}
```

 This input is rejected:

```
{
    "x": 12.50
}
```

 The rejection prevents an implicit binary floating-point representation\
 from entering the deterministic quantitative boundary.

---

 ## 10\. `manifestation`

 The `manifestation` field represents the final output of the execution\
 pipeline.

 The current implementation provides:

```
status
quantities
```

 For a successful deterministic execution:

```
result["manifestation"]["status"]
```

 returns:

```
DETERMINISTIC
```

---

 ## 11\. `UniversalKernel`

 The executable six-component kernel is exposed through:

```
from wyp.kernel import UniversalKernel
```

 ### Constructor

```
UniversalKernel(
    M,
    G,
    A,
    Psi,
    Lambda,
    Proj,
)
```

 ### Example

```
from wyp.kernel import UniversalKernel

kernel = UniversalKernel(
    M="M",
    G="G",
    A="A",
    Psi="Psi",
    Lambda="Lambda",
    Proj="Proj",
)
```

---

 ## 12\. `as_tuple()`

 Returns the six kernel components in canonical order.

```
kernel.as_tuple()
```

 Result:

```
(
    M,
    G,
    A,
    Psi,
    Lambda,
    Proj,
)
```

---

 ## 13\. `component_names()`

 Returns the canonical component names:

```
kernel.component_names()
```

 Result:

```
(
    "M",
    "G",
    "A",
    "Psi",
    "Lambda",
    "Proj",
)
```

---

 ## 14\. `component()`

 Returns a specific kernel component by name.

 Example:

```
kernel.component("Proj")
```

 returns the `Proj` component.

 An unknown component name raises:

```
KeyError
```

---

 ## 15\. `map_components()`

 Applies a transformation function to every kernel component.

 Example:

```
transformed = kernel.map_components(
    lambda component: str(component)
)
```

 The operation returns a new `UniversalKernel`.

 The original kernel remains unchanged.

---

 ## 16\. `DeterministicEngine`

 The execution engine is exposed through:

```
from wyp import DeterministicEngine
```

 ### Constructor

```
DeterministicEngine(kernel)
```

 Example:

```
from wyp import DeterministicEngine
from wyp.api import default_kernel

engine = DeterministicEngine(
    default_kernel()
)
```

---

 ## 17\. Engine Pipeline

 The engine exposes the five processing stages individually:

```
engine.structure(problem)
engine.invariants(structure)
engine.constraints(invariants)
engine.quantities(constraints, problem)
engine.manifestation(quantities)
```

 The complete execution is performed by:

```
engine.solve(problem)
```

---

 ## 18\. `engine.solve()`

 ### Signature

```
engine.solve(
    problem: Mapping[str, Any]
) -> DeterministicResult
```

 The method executes:

```
structure
    ↓
invariants
    ↓
constraints
    ↓
quantities
    ↓
manifestation
```

 and returns a `DeterministicResult`.

---

 ## 19\. `DeterministicResult`

 The result object is an immutable data structure containing:

```
structure
invariants
constraints
quantities
manifestation
```

 Example:

```
result = engine.solve(
    {
        "x": "12",
        "y": "12",
    }
)

print(result.structure)
print(result.invariants)
print(result.constraints)
print(result.quantities)
print(result.manifestation)
```

---

 ## 20\. Decimal Conversion

 The decimal conversion function is exposed internally through:

```
from wyp.decimal_context import decimal
```

 ### Signature

```
decimal(value: object) -> Decimal
```

 Examples:

```
decimal("12.50")
```

 and:

```
decimal(Decimal("12.50"))
```

 are valid.

 Binary floating-point values are rejected:

```
decimal(12.50)
```

 raises:

```
TypeError
```

---

 ## 21\. Deterministic Decimal Context

 The decimal subsystem provides:

```
from wyp.decimal_context import deterministic_context
```

 ### Signature

```
deterministic_context(
    precision: int = 120
)
```

 Example:

```
from wyp.decimal_context import deterministic_context

with deterministic_context(120):
    ...
```

 The default precision is:

```
120
```

 The precision must be strictly positive.

---

 ## 22\. Error Handling

 The WYP API uses explicit Python exceptions for invalid inputs and\
 invalid execution conditions.

 Current principal exceptions include:

```
TypeError
ValueError
KeyError
```

 ### `TypeError`

 Raised when an input cannot be represented according to the deterministic\
 input policy, including binary floating-point values.

 ### `ValueError`

 Raised when deterministic kernel constraints are violated or when an\
 invalid decimal precision is requested.

 ### `KeyError`

 Raised when an unknown kernel component is requested.

---

 ## 23\. Deterministic Execution

 For identical accepted input and identical kernel configuration, the\
 current engine is designed to produce identical results.

 Example:

```
problem = {
    "x": "12.50",
    "y": "144",
}

first = solve(problem)
second = solve(problem)

assert first == second
```

---

 ## 24\. CLI Interface

 The command-line interface is located at:

```
src/wyp/cli/
```

 The package entry point is configured through:

```
wyp.cli.main:main
```

 The installed command is:

```
wyp
```

 The CLI is an interface over the application layer and does not replace\
 the programmatic API.

---

 ## 25\. API Boundary

 The public high-level API is:

```
from wyp import solve
```

 The executable kernel and engine may be accessed directly when an\
 application requires lower-level control.

 The internal implementation may evolve independently provided that the\
 documented public API contract is preserved or explicitly versioned.

---

 ## 26\. Versioning

 The current official application version is:

```
1.0.0
```

 The release identifier is maintained in:

```
VERSION
```

 Release history is maintained in:

```
CHANGELOG.md
```

 API-breaking changes must be associated with an explicit version change.

---

 ## 27\. Formal Verification Layer

 The executable Python API is the application layer.

 Formal mathematical verification is maintained separately in the Lean\
 verification corpus.

 The existence of a Python API does not by itself constitute a formal\
 Lean proof of every executable behavior.

 The two layers are architecturally connected but logically distinct.

---

 ## 28\. Minimal Usage Example

 A complete minimal application is:

```
from wyp import solve

problem = {
    "x": "12",
    "y": "12",
}

result = solve(problem)

print(result["manifestation"])
```

 Expected manifestation:

```
{
    "status": "DETERMINISTIC",
    "quantities": {
        "x": Decimal("12"),
        "y": Decimal("12"),
    },
}
```

---

 ## 29\. API Summary

 The current public application surface is:

```
wyp.solve()
wyp.DeterministicEngine
wyp.kernel.UniversalKernel
wyp.decimal_context.decimal()
wyp.decimal_context.deterministic_context()
```

 The architecture is intentionally modular so that future domain-specific\
 applications can be built above the common WYP execution layer.

