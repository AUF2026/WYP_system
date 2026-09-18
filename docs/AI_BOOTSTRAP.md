WYP AI BOOTSTRAP
1. Scopo

WYP è un sistema matematico modulare nel quale un modello linguistico può interpretare richieste in linguaggio naturale, trasformarle in strutture matematiche eseguibili e coordinare moduli di calcolo e verifica.

Il modello linguistico non costituisce l'autorità matematica finale.

Principio fondamentale:

LLM
  ↓
interpretazione
  ↓
WYP Problem / IR
  ↓
WYP Orchestrator
  ↓
moduli matematici
  ↓
verifica indipendente
  ↓
risultati strutturati
  ↓
LLM
  ↓
risposta finale


Il sistema deve privilegiare risultati calcolati e verificati rispetto a conclusioni generate esclusivamente dal modello linguistico.

2. Architettura canonica
                         USER
                           │
                           ▼
                    ┌─────────────┐
                    │     LLM     │
                    │ interpreter │
                    └──────┬──────┘
                           │
                           ▼
                    WYP Problem / IR
                           │
                           ▼
                  ┌──────────────────┐
                  │ WYP Orchestrator │
                  └────────┬─────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          NUMERIC        SYMBOLIC       FDM
           ENGINE         ENGINE       ENGINE
             │             │             │
             └─────────────┼─────────────┘
                           │
                    ┌──────▼──────┐
                    │ VERIFICATION│
                    └──────┬──────┘
                           │
                           ▼
                    Verified Results
                           │
                           ▼
                          LLM
                           │
                           ▼
                    Natural Response


Il sistema può successivamente integrare:

Lean
LaTeX
PDF
JSON
Markdown
TXT
database matematici
altri verificatori
altri solver

3. Regola fondamentale

L'LLM interpreta.

WYP calcola.

I verificatori controllano.

L'LLM compone la risposta.

L'LLM non deve inventare un risultato quando esiste un modulo WYP capace di calcolarlo o verificarlo.

Esempio:

Utente:
"risolvi x^2 - 4 = 0"

LLM:
  riconosce un'equazione polinomiale

WYP:
  costruisce il problema strutturato

Symbolic Engine:
  calcola x = -2, 2

Verification:
  sostituisce le soluzioni nell'equazione

LLM:
  compone la spiegazione finale

4. WYP Intermediate Representation

Tutte le richieste interpretate dal modello devono poter essere trasformate in una rappresentazione strutturata interna.

Nome concettuale:

WYP-IR


Esempio:

{
  "problem_type": "polynomial_equation",
  "variables": ["x"],
  "domain": "real",
  "expression": "x^2 - 4",
  "condition": {
    "operator": "=",
    "value": "0"
  },
  "requested_action": "solve",
  "required_tools": [
    "symbolic"
  ]
}


WYP-IR deve essere indipendente dal modello linguistico utilizzato.

Il modello può cambiare senza modificare il nucleo matematico.

5. Tipi di problema

Il sistema deve poter classificare almeno:

numeric_calculation
equation
system_of_equations
polynomial
algebra
calculus
linear_algebra
geometry
probability
statistics
number_theory
optimization
symbolic_manipulation
mathematical_proof
formal_proof
open_mathematical_problem
knowledge_query
document_extraction
fdm_problem


La classificazione non deve essere considerata una soluzione matematica.

È soltanto la fase di routing verso gli strumenti appropriati.

6. Tool orchestration

Il modello linguistico deve poter produrre un piano strutturato.

Esempio:

{
  "problem_type": "equation",
  "plan": [
    {
      "tool": "symbolic",
      "operation": "solve"
    },
    {
      "tool": "verification",
      "operation": "substitute"
    }
  ]
}


L'orchestratore WYP decide quali strumenti sono effettivamente disponibili ed eseguibili.

Il modello non deve poter dichiarare autonomamente che un calcolo è stato eseguito.

Deve ricevere il risultato dal tool.

7. Numerical layer

Il numerical layer rimane indipendente dall'LLM.

Componenti esistenti:

NumericEngine
NumericResult
VerificationResult
ExecutionResult


Rappresentazioni supportate:

exact
decimal
float


Il valore numerico effettivo rimane sempre distinto dalla sua rappresentazione testuale.

8. FDM layer

FDM rimane un modulo matematico specializzato.

Relazione canonica:

M_d(U) = Q(U)^d


Componenti:

FDMModel
FDMDerivation
FDMComputation
FDMEngine
FDM verification


L'LLM non deve implementare la relazione FDM.

Deve soltanto riconoscere quando una richiesta richiede il modulo FDM e fornire al modulo i parametri strutturati.

9. Verification-first

Ogni risultato verificabile deve seguire, quando possibile:

compute
  ↓
verify
  ↓
return


Non:

LLM guesses
  ↓
answer


Esempio numerico:

input
 ↓
NumericEngine
 ↓
NumericResult
 ↓
VerificationResult
 ↓
LLM explanation


Esempio FDM:

FDMModel
 ↓
FDMEngine
 ↓
FDMComputation
 ↓
FDM verification
 ↓
LLM

10. Formal verification

Lean può essere utilizzato come verificatore formale.

Architettura:

LLM
 ↓
proposed proof / formalization
 ↓
Lean
 ↓
compiler / checker
 ↓
PASS / FAIL


Il modello non deve dichiarare una dimostrazione formalmente verificata finché il verificatore formale non ha restituito un risultato positivo.

Una dimostrazione proposta dal modello e una dimostrazione verificata da Lean sono due stati differenti.

11. Open mathematical problems

Il sistema deve distinguere tra:

problema risolvibile
problema calcolabile
problema dimostrabile
problema formalmente verificabile
problema aperto
problema non sufficientemente specificato


Esempio:

"risolvi P vs NP"


deve essere classificato come problema matematico aperto, non trasformato artificialmente in una falsa dimostrazione.

Il sistema deve separare:

conoscenza documentata
risultato calcolato
congettura
ipotesi
proposta del modello
dimostrazione verificata

12. Artifact ingestion

WYP deve poter utilizzare materiale matematico esterno.

Formati previsti:

JSON
Lean
LaTeX
PDF
Markdown
TXT


Pipeline:

ARTIFACT
   ↓
IMPORTER
   ↓
EXTRACTOR
   ↓
NORMALIZER
   ↓
WYP-IR
   ↓
KNOWLEDGE / TOOL INPUT


L'obiettivo non è soltanto estrarre testo.

È estrarre struttura matematica.

13. JSON

JSON strutturato può essere utilizzato direttamente come input WYP-IR quando conforme allo schema.

Esempio:

{
  "definitions": [],
  "assumptions": [],
  "variables": [],
  "equations": [],
  "claims": [],
  "requested_action": "prove"
}


Il sistema deve validare lo schema prima dell'esecuzione.

14. LaTeX

LaTeX deve essere trattato come sorgente strutturale.

Esempio:

M_d(U) = Q(U)^d


può essere normalizzato in una rappresentazione interna equivalente.

Il testo LaTeX originale deve comunque essere conservato come sorgente.

Non bisogna perdere la provenienza dell'informazione.

15. Lean

Il codice Lean deve essere conservato come artefatto verificabile.

Pipeline:

Lean source
   ↓
parser / project environment
   ↓
formal declarations
   ↓
verification
   ↓
structured result


L'LLM può:

leggere
spiegare
proporre
trasformare
generare


ma la validità formale deve essere determinata dal sistema Lean.

16. PDF

I PDF devono essere trattati come documenti sorgente.

Pipeline concettuale:

PDF
 ↓
text extraction
 ↓
layout / section extraction
 ↓
formula extraction
 ↓
definition extraction
 ↓
theorem / lemma extraction
 ↓
WYP-IR


Quando l'estrazione è ambigua, il sistema deve conservare l'incertezza invece di inventare contenuto.

Le informazioni estratte devono mantenere la provenienza:

{
  "source": "document.pdf",
  "page": 12,
  "section": "Theorem 3",
  "content": "..."
}

17. Provenance

Ogni informazione derivata da un artifact dovrebbe poter mantenere:

source
source_type
document_id
page
section
line
hash
extraction_method


La provenienza permette di ricostruire da dove è arrivata un'informazione.

18. WYP Artifact

Il sistema dovrà introdurre un contenitore concettuale:

WYPArtifact


Responsabilità:

identità dell'artefatto
sorgente
formato
contenuto originale
contenuto estratto
metadati
provenienza
hash
stato di parsing


L'artefatto originale non deve essere modificato dall'estrazione.

19. WYP Tool

I moduli matematici devono progressivamente convergere verso un'interfaccia comune.

Concettualmente:

WYPTool
 ├── name
 ├── capabilities
 ├── input schema
 ├── execute()
 ├── output schema
 └── verification


Esempi:

NumericTool
SymbolicTool
FDMTool
LeanTool
DocumentTool


Questo permette all'orchestratore di selezionare gli strumenti senza legarsi a una singola implementazione.

20. WYP Execution

Ogni richiesta complessa dovrebbe poter produrre una traccia strutturata:

WYPExecution


Esempio:

{
  "request": "...",
  "problem": {},
  "plan": [],
  "tool_calls": [],
  "results": [],
  "verification": [],
  "warnings": [],
  "final_answer": "..."
}


Questo permette audit, debugging e riproducibilità.

21. LLM backend

L'LLM deve essere un componente sostituibile.

Possibili backend:

remote API
local model
GGUF
llama.cpp
altri runtime compatibili


Il resto del sistema non deve dipendere dal formato del modello.

Architettura:

LLM Adapter
     ↓
WYP-IR
     ↓
WYP Orchestrator


Il modello può quindi essere sostituito senza riscrivere FDM, NumericEngine o Verification.

22. GGUF

GGUF è considerato un possibile formato di distribuzione/esecuzione per un modello locale.

Non deve essere confuso con il solver matematico.

GGUF
  =
modello linguistico

WYP
  =
sistema di interpretazione, calcolo, orchestrazione e verifica


Il GGUF non sostituisce i moduli matematici.

23. Regola di affidabilità

Il sistema deve preferire:

calcolo verificato


rispetto a:

affermazione generata


Esempio:

LLM:
"Il risultato dovrebbe essere 1728."

WYP:
calcola 1728

Verifier:
PASS

LLM:
"Il risultato verificato è 1728."


Se il verifier restituisce FAIL:

LLM:
non deve trasformare il risultato in una certezza.

24. Error handling

Ogni livello deve poter restituire:

success
failure
unsupported
ambiguous
verification_failed
artifact_parse_failed
tool_unavailable


Gli errori non devono essere trasformati in risultati matematici.

25. Security boundary

L'LLM non deve avere accesso arbitrario al sistema operativo.

Le operazioni devono passare attraverso tool autorizzati.

In particolare:

LLM
  ≠
shell arbitraria

LLM
  ≠
accesso filesystem arbitrario

LLM
  ≠
esecuzione codice arbitrario


L'esecuzione deve essere mediata da componenti WYP espliciti.

26. Stato corrente

Componenti già presenti:

FDMModel
FDMDerivation
FDMComputation

NumericEngine

NumericResult
VerificationCheck
VerificationResult
ExecutionResult

FDM verification

WYP HTTP server

WYP public API


Il deployment HTTP è stato portato a esecuzione tramite Python standard library e il servizio è stato verificato in deployment.

Il file wyp/api.py espone il percorso applicativo:

request
 ↓
FDMModel
 ↓
FDMEngine
 ↓
FDMComputation
 ↓
public dictionary

27. Prossima evoluzione

La prossima fase non consiste nel sostituire FDM.

Consiste nell'aggiungere sopra i componenti esistenti:

WYPProblem
WYP-IR
WYPTool
WYPArtifact
WYPExecution
LLM Adapter
WYP Orchestrator


Ordine consigliato:

1. definire WYP-IR
2. definire WYPProblem
3. definire WYPTool
4. definire WYPExecution
5. definire WYPArtifact
6. creare artifact ingestion
7. collegare FDM come tool
8. collegare NumericEngine come tool
9. aggiungere symbolic tool
10. aggiungere verification routing
11. aggiungere Lean integration
12. aggiungere LLM adapter
13. aggiungere local/GGUF backend
14. collegare il solver HTML

28. Principio di continuità

Ogni nuova istanza AI che riprende il progetto deve leggere questo documento prima di modificare il codice.

Prima di intervenire deve:

1. identificare l'architettura esistente
2. leggere i moduli coinvolti
3. non duplicare componenti già presenti
4. non sostituire FDM con il modello linguistico
5. mantenere la verifica indipendente
6. mantenere la provenienza degli artifact
7. modificare un livello alla volta
8. eseguire test prima del deploy
9. verificare il deployment dopo modifiche al boundary HTTP

29. Regola finale

WYP non deve diventare semplicemente:

LLM → risposta


La destinazione architetturale è:

utente
  ↓
LLM
  ↓
WYP-IR
  ↓
orchestrator
  ↓
specialized mathematical tools
  ↓
independent verification
  ↓
structured execution result
  ↓
LLM
  ↓
human-readable answer


Il modello linguistico fornisce comprensione e composizione.

WYP fornisce struttura, calcolo, strumenti, provenienza e verifica.

Questa separazione deve essere mantenuta durante tutte le successive evoluzioni del sistema.
