````
# WYP CLI

## Overview

The WYP command-line interface provides a direct terminal interface to the
WYP deterministic engine.

The CLI is implemented in:

```text
src/wyp/cli/
├── __init__.py
└── main.py
````

 The CLI is an application-layer interface. It does not replace the formal\
 mathematical verification layer maintained separately in the AUF2026 corpus.

---

 ## Command

 The primary command is:

```
wyp
```

 The command provides access to the deterministic WYP execution pipeline.

 The conceptual execution chain is:

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

---

 ## Input

 The CLI accepts problem data and passes it to the public WYP API.

 The public API entry point is:

```
from wyp import solve
```

 The API accepts a mapping representing the problem:

```
problem = {
    "x": "12",
    "y": "12",
}

result = solve(problem)
```

 Numerical values intended for deterministic quantitative processing should be\
 provided through decimal-compatible representations.

 Binary floating-point values are not part of the deterministic numerical\
 interface.

---

 ## Execution Model

 A WYP execution proceeds through five application-level stages.

 ### 1\. Structure

 The input problem is associated with the universal kernel and represented as\
 the structural input to the computation.

 The executable kernel exposes:

```
U_F = (M, G, A, Psi, Lambda, Proj)
```

 ### 2\. Invariants

 The engine evaluates structural properties associated with the represented\
 kernel and records the resulting invariants.

 ### 3\. Constraints

 The identified invariants are used to establish the constraints required for\
 the deterministic execution.

 ### 4\. Quantities

 Quantitative input is converted into the deterministic numerical\
 representation used by the application layer.

 The WYP numerical layer uses:

```
decimal.Decimal
```

 Binary floating-point input is rejected by the deterministic decimal\
 conversion layer.

 ### 5\. Manifestation

 The engine produces the final application-level result.

 A successful deterministic execution reports:

```
DETERMINISTIC
```

---

 ## Python API

 The CLI is backed by the public WYP API.

 The principal entry point is:

```
from wyp import solve
```

 Example:

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

 The returned object contains:

```
structure
invariants
constraints
quantities
manifestation
```

---

 ## Kernel

 The executable representation of the six-component universal kernel is:

```
U_F = (M, G, A, Psi, Lambda, Proj)
```

 The corresponding Python object is:

```
UniversalKernel(
    M=...,
    G=...,
    A=...,
    Psi=...,
    Lambda=...,
    Proj=...,
)
```

 The kernel provides explicit access to its six components and preserves their\
 ordering in its tuple representation.

---

 ## Deterministic Numerical Policy

 WYP does not use binary floating-point arithmetic for deterministic\
 quantitative processing.

 The application layer uses:

```
from decimal import Decimal
```

 Valid deterministic numerical representations include decimal strings:

```
"12"
"12.50"
"0.125"
```

 These are converted to:

```
Decimal("12")
Decimal("12.50")
Decimal("0.125")
```

 A Python binary floating-point value such as:

```
12.5
```

 is rejected by the deterministic conversion layer.

 This policy prevents implicit conversion from binary floating-point\
 representations into the deterministic decimal numerical layer.

---

 ## Architecture Boundary

 The WYP CLI belongs to the executable application layer:

```
User
  ↓
WYP CLI
  ↓
WYP API
  ↓
Deterministic Engine
  ↓
Universal Kernel
```

 The formal mathematical verification layer remains a separate artifact:

```
Formal Mathematical Corpus
        ↓
Lean Verification
        ↓
Verified Mathematical Results
```

 The application implementation should therefore not be interpreted as a\
 replacement for the Lean verification corpus.

 The two layers have distinct purposes:

```
FORMAL LAYER
mathematical definitions
        ↓
formal proofs
        ↓
machine verification

APPLICATION LAYER
problem input
        ↓
deterministic engine
        ↓
executable manifestation
```

---

 ## Reproducibility

 A WYP execution should be reproducible when supplied with the same problem\
 representation and the same application version.

 For deterministic quantitative inputs, decimal representations should be\
 specified explicitly rather than through binary floating-point values.

 Example:

```
problem = {
    "x": "12",
    "y": "12",
}
```

 The same input is expected to produce the same application-level result under\
 the same software version and execution configuration.

---

 ## Scope

 The CLI is intentionally thin.

 Its responsibility is to provide an accessible interface to the WYP\
 application engine while keeping the computational kernel, public API,\
 numerical policy and formal verification corpus as separately identifiable\
 layers.

 The CLI therefore provides an operational interface to WYP without changing\
 the mathematical definitions or formal verification results on which the\
 broader AUF2026 architecture is based.

