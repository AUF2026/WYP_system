Perfetto. **Prossimo passo unico: creiamo `docs/` e il primo documento tecnico.**

 Alla radice:

```
WYP_system/
├── docs/
│   └── architecture.md    ← ADESSO
├── src/
├── examples/
├── tests/
├── pyproject.toml
├── VERSION
├── CHANGELOG.md
├── README.md
├── license.md
└── COMMERCIAL_LICENSE.md
```

 Crea la cartella `docs/`, poi il file:

```
docs/architecture.md
```

 Incolla **esattamente questo**:

````
# WYP System — Architecture

## 1. Overview

WYP? — What's Your Problem? It's Deterministically Solved!

is the executable application layer of the AUF2026 / FAURE_CORE_2026
architecture.

The system is organized as a deterministic processing pipeline:

```text
structure
    ↓
invariants
    ↓
constraints
    ↓
quantities
    ↓
manifestation
````

 Each stage receives the result of the preceding stage and produces the\
 next explicitly defined representation.

---

 ## 2\. Application Kernel

 The executable kernel is represented by six structural components:

```
U_F = (M, G, A, Psi, Lambda, Proj)
```

 These components are represented by the immutable `UniversalKernel`\
 object.

 The implementation does not require a particular encoding of the\
 underlying application state.

---

 ## 3\. Software Layers

 The package is organized into the following principal layers:

```
wyp
│
├── kernel
│   └── UniversalKernel
│
├── decimal_context
│   └── deterministic decimal arithmetic
│
├── engine
│   ├── structure
│   ├── invariants
│   ├── constraints
│   ├── quantities
│   └── manifestation
│
├── api
│   └── solve()
│
└── cli
    └── command-line interface
```

---

 ## 4\. UniversalKernel

 `UniversalKernel` is an immutable executable representation of the six\
 kernel components.

 The component ordering is fixed:

```
M
G
A
Psi
Lambda
Proj
```

 The kernel provides:

 - complete tuple representation;
- component-name enumeration;
- component lookup;
- component-wise structural transformation.

 The kernel object is implemented as a frozen dataclass.

---

 ## 5\. Deterministic Engine

 `DeterministicEngine` executes the WYP processing pipeline.

 The execution sequence is:

```
problem
   ↓
structure()
   ↓
invariants()
   ↓
constraints()
   ↓
quantities()
   ↓
manifestation()
   ↓
DeterministicResult
```

 The complete result is represented by the immutable\
 `DeterministicResult` structure.

---

 ## 6\. Structure Stage

 The structure stage receives the input problem and constructs its\
 structural representation.

 The resulting representation contains:

 - the problem data;
- the kernel tuple;
- the six kernel component identifiers.

 The purpose of this stage is to establish the structural object on which\
 the subsequent stages operate.

---

 ## 7\. Invariants Stage

 The invariants stage evaluates structural properties of the current\
 representation.

 The initial executable implementation exposes:

```
component_count
representation_invariant
structural_identity
```

 These values provide the structural conditions consumed by the\
 constraint stage.

---

 ## 8\. Constraints Stage

 The constraints stage derives explicit execution conditions from the\
 invariants.

 The initial implementation requires:

```
representation_invariant = True
structural_identity      = True
component_count          = 6
```

 The resulting constraint object contains:

```
valid
required_component_count
```

 A problem violating the deterministic kernel constraints is rejected\
 before quantitative manifestation.

---

 ## 9\. Quantities Stage

 Quantitative values are represented using Python's\
 `decimal.Decimal`.

 Binary floating-point values are explicitly rejected by the deterministic\
 conversion layer.

 For example:

```
"12.50"
```

 is converted directly to:

```
Decimal("12.50")
```

 whereas:

```
12.50
```

 is rejected as a binary floating-point input.

 This establishes an explicit numerical boundary between accepted decimal\
 representations and forbidden binary floating-point inputs.

---

 ## 10\. Decimal Context

 The decimal subsystem provides an explicit precision context.

 The default precision is:

```
120
```

 The precision can be explicitly configured for a computation.

 The implementation uses Python's standard-library `decimal` module and\
 does not depend on third-party numerical packages for the core\
 quantitative layer.

---

 ## 11\. Manifestation Stage

 The manifestation stage constructs the final executable result.

 The initial manifestation contains:

```
status
quantities
```

 with the deterministic status:

```
DETERMINISTIC
```

 The manifestation therefore represents the final output of the WYP\
 pipeline.

---

 ## 12\. Public API

 The public API exposes:

```
from wyp import solve
```

 A problem can then be submitted as:

```
result = solve(
    {
        "x": "12",
        "y": "12",
    }
)
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

 ## 13\. Command-Line Layer

 The command-line interface is located under:

```
src/wyp/cli/
```

 and is intentionally separated from the core engine.

 The CLI is therefore an interface layer rather than part of the\
 mathematical kernel itself.

 The package entry point is configured through:

```
wyp.cli.main:main
```

---

 ## 14\. Formal Verification Boundary

 The executable Python layer and the formal Lean verification corpus are\
 distinct layers.

 The Python implementation provides:

 - executable application logic;
- deterministic data handling;
- API access;
- command-line access;
- reproducible execution.

 The Lean corpus provides the formal mathematical verification layer.

 The two layers are therefore related architecturally but are not\
 implicitly identified.

---

 ## 15\. Reproducibility

 The WYP application is designed so that identical accepted inputs,\
 identical kernel configuration, and identical execution configuration\
 produce identical results.

 The test suite under:

```
tests/
```

 provides automated regression checks for the executable application\
 layer.

 Reproducibility assets and formal verification materials may be\
 maintained separately from the runtime package.

---

 ## 16\. Design Principle

 The principal architectural sequence is:

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

 This sequence defines the current executable WYP processing model.

 The architecture is intentionally modular so that additional\
 structural invariants, constraints, quantitative operators, and\
 manifestation mechanisms can be introduced without changing the\
 fundamental package organization.

---

 ## 17\. Package Layout

 The canonical source layout is:

```
WYP_system/
│
├── src/
│   └── wyp/
│       ├── __init__.py
│       ├── api.py
│       ├── decimal_context.py
│       ├── engine.py
│       ├── kernel.py
│       │
│       └── cli/
│           ├── __init__.py
│           └── main.py
│
├── examples/
│   └── basic_problem.py
│
├── tests/
│   └── test_wyp.py
│
├── docs/
│   └── architecture.md
│
├── pyproject.toml
├── VERSION
├── CHANGELOG.md
├── README.md
├── license.md
└── COMMERCIAL_LICENSE.md
```

---

 ## 18\. Extension Model

 Future application modules should depend on the public API and defined\
 kernel interfaces rather than duplicating the internal execution\
 pipeline.

 The intended extension direction is:

```
UniversalKernel
       ↓
DeterministicEngine
       ↓
Public API
       ↓
Applications
       ↓
Domain-specific interfaces
```

 This permits domain-specific applications to be developed while\
 preserving a common WYP execution architecture.

---

 ## 19\. Current Release

 Current official application version:

```
1.0.0
```

 The authoritative release identifier is maintained in:

```
VERSION
```

 and the release history is maintained in:

```
CHANGELOG.md
```

