# WYP AI BOOTSTRAP

 ## 0\. SCOPO DI QUESTO FILE

 Questo file è il punto di ripresa del progetto per una nuova istanza AI.

 Se una nuova istanza viene avviata, deve leggere questo file prima di modificare codice.

 NON ripartire da zero.

 NON ricreare componenti già presenti.

 NON cambiare architettura senza prima verificare lo stato descritto qui.

 Il progetto in costruzione è WYP, parte dell'ecosistema AUF2026 / AOS-PRIVATE-CORE.

 Obiettivo generale:

 > costruire un sistema WYP pubblico, consultabile e utilizzabile tramite una pagina GitHub Pages, mantenendo tutta la matematica, i teoremi, il solver e la verifica delle licenze nella repository privata.

 L'architettura corrente è già evoluta oltre il semplice FDM endpoint.

 Il private core dispone ora di una separazione esplicita fra:

 - interpretazione del linguaggio naturale;
- problema strutturato;
- routing del solver;
- calcolo deterministico;
- risultato canonico;
- composizione della risposta tramite LLM.

 Il modello linguistico NON è l'autorità matematica.

 Il solver deterministico rimane l'autorità sul risultato computazionale.

---

 # 1\. ARCHITETTURA DEFINITIVA

 L'architettura corrente è:

```
                         PUBLIC INTERNET
                                │
                                ▼
                   GitHub Pages — PUBLIC REPO
                   https://auf2026.github.io/WYP_system/
                                │
                                │
                         HTML / CSS / JS
                                │
                   ┌────────────┴────────────┐
                   │                         │
                   ▼                         ▼
            Jotform contact form       WYP Solver / Tester
                                           │
                                           ▼
                              Cloudflare Worker
                              https://wyp.auf2026.workers.dev/
                                           │
                                           ▼
                              AOS PRIVATE CORE
                              Render deployment
                              https://aos-private-core.onrender.com
                                           │
                                           ▼
                                  WYP HTTP SERVER
                                           │
                                           ▼
                                NATURAL LANGUAGE REQUEST
                                           │
                                           ▼
                                   LLM INTERPRETER
                                           │
                                           ▼
                                    WYPProblem
                                           │
                                           ▼
                                  SOLVER ROUTER
                                           │
                         ┌─────────────────┼─────────────────┐
                         │                 │                 │
                         ▼                 ▼                 ▼
                        FDM           NUMERICAL          THEOREMS
                         │              MODULES             │
                         │                 │                │
                         └─────────────────┼────────────────┘
                                           │
                                           ▼
                                     SolverResult
                                           │
                                           ▼
                                  VERIFICATION
                                           │
                                           ▼
                                  RESPONSE LLM
                                           │
                                           ▼
                                   FINAL ANSWER
```

 Il principio fondamentale è:

```
USER
  ↓
LLM / INTERPRETER
  ↓
WYPProblem
  ↓
SOLVER ROUTER
  ↓
DETERMINISTIC SOLVER
  ↓
SolverResult
  ↓
RESPONSE LLM
  ↓
USER
```

 Il modello linguistico interpreta e compone.

 WYP calcola.

 I verificatori verificano.

---

 # 2\. REPOSITORY PUBBLICA

 Repository:

```
AUF2026/WYP_system
```

 GitHub Pages:

```
https://auf2026.github.io/WYP_system/
```

 Questa repository è PUBBLICA.

 Deve contenere solamente materiale pubblico, ad esempio:

```
index.html
about.html
research.html
documentation.html
license.html
README.md
LICENSE.md
assets/
css/
js/
images/
docs/
```

 La repository pubblica NON deve contenere:

 - private key;
- license signing key;
- token di licenza;
- segreti Render;
- credenziali Cloudflare;
- solver Python privato;
- implementazioni matematiche protette;
- sorgenti Lean protetti;
- teoremi privati;
- copie della logica interna del solver.

 Il JavaScript pubblico deve essere solamente un client HTTP/UI.

 Il frontend pubblico non deve duplicare il motore matematico.

---

 # 3\. REPOSITORY PRIVATA

 Repository privata:

```
https://github.com/AUF2026/AOS-PRIVATE-CORE
```

 Questa è la repository che contiene il vero motore WYP.

 Struttura corrente rilevante:

```
src/wyp/
    core/
        __init__.py
        interpreter.py
        kernel.py
        llm.py
        numeric.py
        pipeline.py
        problem.py
        result.py
        router.py

    fdm/
    theorems/
    license/

    __init__.py
    api.py
    server.py
    requirements.txt
```

 La matematica deve rimanere qui.

 In particolare:

```
wyp.fdm
wyp.theorems
Lean sources
Python mathematical implementation
solver implementation
license verification
```

 Il frontend pubblico NON deve duplicare queste strutture.

---

 # 4\. DEPLOY RENDER

 URL del private core:

```
https://aos-private-core.onrender.com
```

 Il deploy corrente FUNZIONA.

 Ultimo deploy verificato:

```
==> Build successful 🎉
==> Deploying...
[WYP] service=WYP
[WYP] component=FDM
[WYP] version=1.0.0
[WYP] listening=http://0.0.0.0:10000
[WYP] HTTP backend ready
[WYP] 127.0.0.1 - "HEAD / HTTP/1.1" 200 -
[WYP] 127.0.0.1 - "GET / HTTP/1.1" 200 -
==> Your service is live 🎉
```

 Il servizio è attualmente online.

 Runtime verificato:

```
Python 3.14.3
```

 Build command funzionante:

```
pip install --upgrade pip && pip install -r src/wyp/requirements.txt
```

 Start command funzionante:

```
PYTHONPATH=src python -m wyp.server
```

 Il requirements attuale non utilizza FastAPI.

 La dipendenza crittografica attuale include:

```
cryptography
cffi
pycparser
```

 NON reintrodurre FastAPI automaticamente.

 NON modificare il runtime HTTP senza necessità.

---

 # 5\. PRIVATE CORE HTTP

 Il private core risponde almeno a:

```
GET /
```

 e:

```
HEAD /
```

 Entrambi sono stati verificati con:

```
200
```

 È presente anche:

```
/health
```

 Il percorso applicativo deve progressivamente convergere verso:

```
HTTP request
    ↓
request validation
    ↓
license verification
    ↓
WYP interpretation
    ↓
WYPProblem
    ↓
solver routing
    ↓
deterministic solver
    ↓
verification
    ↓
SolverResult
    ↓
response composition
    ↓
JSON response
```

 Il server non deve diventare il luogo dove duplicare la matematica.

---

 # 6\. CLOUDFLARE WORKER

 Worker pubblico:

```
https://wyp.auf2026.workers.dev/
```

 Il Worker è un gateway HTTP.

 Architettura:

```
Browser
   ↓
Cloudflare Worker
   ↓
https://aos-private-core.onrender.com
```

 Il Worker NON deve contenere:

 - private key;
- license key;
- verification key;
- solver;
- matematica;
- codice Lean;
- implementazione FDM;
- logica protetta.

 Il Worker deve fare solamente:

 1. ricevere HTTP;
2. gestire CORS;
3. validare superficialmente il JSON;
4. inoltrare la richiesta al private core;
5. restituire la risposta del private core.

 Il Worker non deve diventare un secondo solver.

---

 # 7\. LICENSING

 La verifica licenze è SERVER-SIDE.

 Il modulo è:

```
wyp/license
```

 La verifica utilizza Ed25519.

 Il repository NON contiene la private signing key.

 Il private core utilizza variabili d'ambiente.

 Variabili:

```
WYP_LICENSE_KEY
WYP_LICENSE_PUBLIC_KEY
```

 La funzione principale è:

```
require_license()
```

 La verifica comprende:

 - presenza del token;
- struttura del token;
- decoding Base64URL;
- parsing JSON;
- verifica firma Ed25519;
- verifica product;
- verifica claims;
- verifica `issued_at`;
- verifica `expires_at`;
- verifica scadenza.

 NON copiare token di licenza nel frontend.

 NON inserire la licenza nel Worker.

 NON inserire la licenza in Git.

 La configurazione effettiva deve rimanere sul private core / Render.

---

 # 8\. PUBLIC KEY

 La public verification key è un dato pubblico crittografico.

 La verifica della licenza rimane comunque responsabilità del private core.

 Il browser NON deve conoscere la private signing key.

 Non inserire materiale crittografico nel frontend senza una ragione architetturale precisa.

---

 # 9\. SERVER.PY

 Il server non dipende da FastAPI.

 La struttura corrente è:

```
HTTP request
    ↓
request validation
    ↓
license verification
    ↓
WYP execution boundary
    ↓
solver
    ↓
FDM / theorems / future modules
    ↓
JSON response
```

 Il server non deve contenere la matematica.

 La matematica canonica rimane nei moduli:

```
wyp.fdm
wyp.theorems
```

 e nei relativi sorgenti matematici.

---

 # 10\. WYP CORE

 Il core WYP è ora un livello architetturale reale.

 Struttura:

```
src/wyp/core/

    __init__.py
    interpreter.py
    kernel.py
    llm.py
    numeric.py
    pipeline.py
    problem.py
    result.py
    router.py
```

 Responsabilità:

```
problem.py
    ↓
strutture canoniche

interpreter.py
    ↓
natural language → WYPProblem

llm.py
    ↓
LLM boundary

router.py
    ↓
WYPProblem → solver

pipeline.py
    ↓
interpret → solve → compose

result.py
    ↓
risultati numerici canonici

numeric.py
    ↓
supporto numerico

kernel.py
    ↓
AOSKernel
```

 Il core non deve implementare direttamente la matematica specifica dei domini.

---

 # 11\. WYPProblem

 `WYPProblem` è la rappresentazione canonica di un problema.

 Definita in:

```
src/wyp/core/problem.py
```

 Struttura:

```
WYPProblem
    ├── intent
    ├── domain
    ├── problem
    ├── constraints
    └── metadata
```

 Esempio:

```
{
  "intent": "compute",
  "domain": "fdm",
  "problem": {
    "modulus": 12,
    "dimension": 3
  },
  "constraints": {},
  "metadata": {}
}
```

 Il core non interpreta matematicamente il contenuto di `problem`.

 Il dominio selezionato è responsabile dell'interpretazione dei propri parametri.

---

 # 12\. WYP INTERPRETER

 Il modulo:

```
src/wyp/core/interpreter.py
```

 definisce il confine:

```
natural language
    ↓
WYPProblem
```

 Interfaccia principale:

```
WYPInterpreter
```

 Implementazioni/adapters presenti:

```
StructuredProblemInterpreter
CallableInterpreter
```

 L'interpreter non calcola.

 Il suo unico compito è produrre un `WYPProblem` valido.

 Questo permette di sostituire successivamente:

```
remote LLM
local LLM
GGUF
deterministic parser
hybrid interpreter
```

 senza modificare il solver.

---

 # 13\. LLM BOUNDARY

 Il modulo:

```
src/wyp/core/llm.py
```

 definisce il contratto LLM.

 Sono presenti:

```
WYPLLMError
WYPLLMOutputError
WYPLLMBackend
WYPProblemLLM
WYPResponseLLM
```

 Il backend astratto espone:

```
generate(...)
```

 Il core NON dipende da:

```
OpenAI
Anthropic
GGUF
llama.cpp
transformers
specific inference server
```

 Il modello può essere sostituito senza riscrivere il nucleo matematico.

 Architettura:

```
LLM backend
    ↓
WYPProblemLLM
    ↓
WYPProblem
```

 e:

```
SolverResult
    ↓
WYPResponseLLM
    ↓
user-facing answer
```

 Il risultato del solver rimane sempre autorevole.

---

 # 14\. LLM PROBLEM INTERPRETATION

 L'LLM interpreter deve produrre esclusivamente una struttura compatibile con `WYPProblem`.

 Contratto concettuale:

```
{
  "intent": "string",
  "domain": "string",
  "problem": {},
  "constraints": {},
  "metadata": {}
}
```

 Il testo libero dell'LLM NON deve essere passato direttamente al solver.

 La pipeline è:

```
USER REQUEST
    ↓
LLM
    ↓
JSON
    ↓
validation
    ↓
WYPProblem
    ↓
solver
```

 Se il JSON non è valido:

```
WYP LLM OUTPUT ERROR
```

 e il solver non viene eseguito.

---

 # 15\. SOLVER ROUTER

 Il modulo:

```
src/wyp/core/router.py
```

 contiene:

```
WYPSolverRouter
```

 Il router non implementa matematica.

 Registra solver con:

```
(domain, intent)
```

 e risolve il solver appropriato.

 Esempio corrente:

```
fdm / compute
fdm / solve
```

 entrambi instradati verso:

```
solve_fdm_problem()
```

 Il router è quindi:

```
WYPProblem
    ↓
(domain, intent)
    ↓
registered solver
```

---

 # 16\. FDM ADAPTER

 Il router contiene un adapter verso l'API FDM esistente.

 Flusso:

```
WYPProblem
    ↓
solve_fdm_problem()
    ↓
wyp.api.solve()
    ↓
FDM
    ↓
SolverResult
```

 L'adapter non implementa la matematica FDM.

 La matematica rimane nel sottosistema:

```
wyp.fdm
```

 Questo permette di aggiungere in seguito:

```
algebra
number_theory
linear_algebra
statistics
optimization
theorems
Lean
symbolic
```

 senza trasformare il router in un solver monolitico.

---

 # 17\. PIPELINE

 Il modulo:

```
src/wyp/core/pipeline.py
```

 implementa il confine di esecuzione naturale:

```
user request
    ↓
WYPInterpreter
    ↓
WYPProblem
    ↓
deterministic solver
    ↓
SolverResult
    ↓
WYPResponseLLM
    ↓
final answer
```

 La classe principale è:

```
WYPPipeline
```

 La pipeline esegue rigorosamente:

```
1. interpretation
2. deterministic solving
3. response composition
```

 Il solver deve restituire:

```
SolverResult
```

 Il composer riceve il `SolverResult` come dato autorevole.

---

 # 18\. SolverResult

 Il risultato canonico è:

```
SolverResult
```

 e contiene:

```
success
solver
value
answer
verification
warnings
metadata
```

 Regola fondamentale:

```
value = authoritative result
```

 `answer` è solamente testo di presentazione.

 Il modello linguistico non può sostituire `value`.

 Un risultato:

```
SolverResult(success=False)
```

 deve rimanere un fallimento.

 Non deve essere trasformato dall'LLM in una risposta matematica apparentemente certa.

---

 # 19\. WYP FDM

 Esiste un modello FDM canonico.

 Relazione matematica:

```
M_d(U) = Q(U)^d
```

 Componenti esistenti:

```
FDMModel
FDMDerivation
FDMComputation
FDMEngine
FDM verification
```

 L'LLM non implementa la relazione FDM.

 Deve soltanto:

```
riconoscere la richiesta
    ↓
costruire WYPProblem
    ↓
fornire parametri strutturati
```

 Il calcolo resta nel modulo FDM.

---

 # 20\. THEOREMS

 La repository privata contiene:

```
wyp.theorems
```

 e i relativi materiali matematici/formali.

 I teoremi sono parte del motore privato.

 La pagina pubblica può descrivere concettualmente:

 - ricerca;
- metodo;
- formalizzazione;
- verifica;
- teoremi;
- FDM;
- solver.

 Non deve contenere le implementazioni private.

---

 # 21\. VERIFICATION-FIRST

 Ogni risultato verificabile deve seguire, quando possibile:

```
compute
    ↓
verify
    ↓
return
```

 Non:

```
LLM guesses
    ↓
answer
```

 Esempio:

```
input
    ↓
solver
    ↓
SolverResult
    ↓
verification
    ↓
LLM explanation
```

 La verifica deve essere separata dalla composizione linguistica.

---

 # 22\. FORMAL VERIFICATION / LEAN

 Lean può essere utilizzato come verificatore formale.

 Architettura:

```
LLM
    ↓
proposed formalization
    ↓
Lean
    ↓
compiler / checker
    ↓
PASS / FAIL
```

 Il modello non deve dichiarare una dimostrazione formalmente verificata finché il verificatore formale non ha restituito un risultato positivo.

 Distinguere sempre:

```
proposta del modello
```

 da:

```
formalmente verificato
```

---

 # 23\. OPEN MATHEMATICAL PROBLEMS

 Il sistema deve distinguere tra:

```
problema risolvibile
problema calcolabile
problema dimostrabile
problema formalmente verificabile
problema aperto
problema non sufficientemente specificato
```

 Esempio:

```
"risolvi P vs NP"
```

 non deve essere trasformato artificialmente in una falsa dimostrazione.

 Il sistema deve separare:

```
conoscenza documentata
risultato calcolato
congettura
ipotesi
proposta del modello
dimostrazione verificata
```

 Per problemi aperti, il sistema può:

 - identificare il problema;
- spiegare lo stato della conoscenza;
- consultare materiale fornito;
- analizzare definizioni;
- eseguire sotto-problemi calcolabili;
- verificare argomenti formali quando possibile.

 Non deve inventare una soluzione.

---

 # 24\. ARTIFACT INGESTION

 WYP deve poter utilizzare materiale matematico esterno.

 Formati previsti:

```
JSON
Lean
LaTeX
PDF
Markdown
TXT
```

 Pipeline:

```
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
```

 L'obiettivo non è solamente estrarre testo.

 È estrarre struttura matematica utilizzabile dai moduli WYP.

---

 # 25\. JSON INGESTION

 JSON strutturato può essere utilizzato direttamente come input quando conforme allo schema previsto.

 Esempio:

```
{
  "definitions": [],
  "assumptions": [],
  "variables": [],
  "equations": [],
  "claims": [],
  "requested_action": "prove"
}
```

 Il sistema deve validare lo schema prima dell'esecuzione.

 JSON può inoltre rappresentare:

```
WYPProblem
tool input
tool output
verification result
artifact metadata
execution trace
```

---

 # 26\. LATEX INGESTION

 LaTeX deve essere trattato come sorgente strutturale.

 Esempio:

```
M_d(U) = Q(U)^d
```

 può essere normalizzato in una rappresentazione interna equivalente.

 Il testo LaTeX originale deve comunque essere conservato come sorgente.

 Non bisogna perdere la provenienza dell'informazione.

---

 # 27\. LEAN INGESTION

 Il codice Lean deve essere conservato come artefatto verificabile.

 Pipeline:

```
Lean source
    ↓
parser / project environment
    ↓
formal declarations
    ↓
verification
    ↓
structured result
```

 L'LLM può:

```
leggere
spiegare
proporre
trasformare
generare
```

 ma la validità formale deve essere determinata dal sistema Lean.

---

 # 28\. PDF INGESTION

 I PDF devono essere trattati come documenti sorgente.

 Pipeline concettuale:

```
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
```

 Quando l'estrazione è ambigua, il sistema deve conservare l'incertezza invece di inventare contenuto.

 Le informazioni estratte devono mantenere la provenienza:

```
{
  "source": "document.pdf",
  "page": 12,
  "section": "Theorem 3",
  "content": "..."
}
```

---

 # 29\. PROVENANCE

 Ogni informazione derivata da un artifact dovrebbe poter mantenere:

```
source
source_type
document_id
page
section
line
hash
extraction_method
```

 La provenienza permette di ricostruire da dove è arrivata un'informazione.

 Non perdere la provenienza durante:

```
PDF → extraction
LaTeX → normalization
Lean → parsing
JSON → validation
```

---

 # 30\. WYP ARTIFACT

 Il sistema dovrà utilizzare un contenitore concettuale:

```
WYPArtifact
```

 Responsabilità:

```
identità dell'artefatto
sorgente
formato
contenuto originale
contenuto estratto
metadati
provenienza
hash
stato di parsing
```

 L'artefatto originale non deve essere modificato dall'estrazione.

 La versione normalizzata deve essere separata dalla sorgente.

---

 # 31\. WYP TOOL

 I moduli matematici devono progressivamente convergere verso un'interfaccia comune.

 Concettualmente:

```
WYPTool
    ├── name
    ├── capabilities
    ├── input schema
    ├── execute()
    ├── output schema
    └── verification
```

 Esempi:

```
NumericTool
SymbolicTool
FDMTool
LeanTool
DocumentTool
TheoremTool
```

 Il router/orchestrator deve poter selezionare gli strumenti senza legarsi a una singola implementazione.

---

 # 32\. WYP EXECUTION

 Ogni richiesta complessa dovrebbe poter produrre una traccia strutturata:

```
WYPExecution
```

 Esempio:

```
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
```

 Questo permette:

```
audit
debugging
riproducibilità
provenance
verification tracing
```

 La pipeline corrente rappresenta già una prima implementazione di questo concetto attraverso:

```
WYPPipelineResult
```

---

 # 33\. LLM BACKEND

 L'LLM deve essere un componente sostituibile.

 Possibili backend:

```
remote API
local model
GGUF
llama.cpp
transformers
altri runtime compatibili
```

 Il resto del sistema non deve dipendere dal formato del modello.

 Architettura:

```
LLM Backend
    ↓
WYPLLMBackend
    ↓
WYPProblemLLM
    ↓
WYPProblem
    ↓
WYP solver
```

 e:

```
SolverResult
    ↓
WYPResponseLLM
    ↓
final answer
```

 Il modello può quindi essere sostituito senza riscrivere FDM, NumericEngine, verification o router.

---

 # 34\. GGUF

 GGUF è un possibile formato di distribuzione/esecuzione per un modello locale.

 Non deve essere confuso con il solver matematico.

```
GGUF
    =
modello linguistico
```

 mentre:

```
WYP
    =
interpretazione
calcolo
orchestrazione
verifica
```

 Il GGUF NON sostituisce i moduli matematici.

 L'integrazione GGUF non deve essere inserita direttamente in:

```
problem.py
router.py
pipeline.py
```

 Il backend deve implementare il contratto LLM già definito.

---

 # 35\. REGOLA DI AFFIDABILITÀ

 Il sistema deve preferire:

```
calcolo verificato
```

 rispetto a:

```
affermazione generata
```

 Esempio:

```
LLM:
"Il risultato dovrebbe essere 1728."

WYP:
calcola 1728

Verifier:
PASS

LLM:
"Il risultato verificato è 1728."
```

 Se il verifier restituisce FAIL:

```
LLM:
non deve trasformare il risultato in una certezza.
```

---

 # 36\. ERROR HANDLING

 Ogni livello deve poter restituire stati distinti:

```
success
failure
unsupported
ambiguous
verification_failed
artifact_parse_failed
tool_unavailable
```

 Gli errori non devono essere trasformati in risultati matematici.

 La pipeline corrente distingue almeno:

```
WYPPipelineInterpretationError
WYPPipelineSolverError
WYPPipelineCompositionError
```

 Il boundary LLM distingue:

```
WYPLLMError
WYPLLMOutputError
```

 Il router distingue:

```
WYPSolverError
```

 Questi confini devono essere mantenuti.

---

 # 37\. SECURITY BOUNDARY

 L'LLM non deve avere accesso arbitrario al sistema operativo.

 Le operazioni devono passare attraverso tool autorizzati.

 In particolare:

```
LLM
  ≠
shell arbitraria

LLM
  ≠
accesso filesystem arbitrario

LLM
  ≠
esecuzione codice arbitrario
```

 L'esecuzione deve essere mediata da componenti WYP espliciti.

 Artifact ingestion deve essere trattata come input non affidabile.

---

Sì. Ho verificato prima la pagina pubblica: è effettivamente online e contiene la homepage/form WYP con `IDENT`, email, settore, problematica e `EXECUTE WYP`.  Auf2026

 Riprendiamo **esattamente dal punto 38**, senza riscrivere ciò che viene prima.

 Bootstrap — prosecuzione dal punto 38

## 38\. PAGINA PUBBLICA INDEX

 La pagina:

 https://auf2026.github.io/WYP\_system/

 è la homepage pubblica.

 Contiene:

 - interfaccia pubblica WYP;
- identificazione dell'azienda / brand;
- canale email;
- selezione del dominio / settore;
- campo per la descrizione della problematica;
- comando `EXECUTE WYP`;
- area di analisi `WYP ENGINE — DETERMINISTIC ANALYSIS`;
- area `PROBLEM INPUT`;
- comando `ANALYZE PROBLEM`;
- collegamento al backend WYP.

 La pagina pubblica costituisce quindi il **frontend di ingresso** del sistema.

 Il frontend non deve contenere la logica matematica autorevole.

 Il flusso corretto è:

```
pagina pubblica
    ->
richiesta utente
    ->
backend WYP
    ->
interpretazione
    ->
WYPProblem
    ->
solver deterministico
    ->
SolverResult
    ->
composizione risposta
    ->
frontend
```

 La pagina pubblica può quindi essere utilizzata come punto di ingresso per richieste espresse in linguaggio naturale.

 Esempi di richieste che il sistema dovrà progressivamente poter interpretare:

```
risolvi x + 5 = 12

risolvi il sistema ...

risolvi P vs NP

analizza questo problema ...

calcola ...

verifica ...
```

 La pagina non deve implementare direttamente tali solver.

---

 ## 39\. BACKEND WYP OPERATIVO

 Il backend WYP è attualmente pubblicato tramite Render.

 Servizio:

 https://aos-private-core.onrender.com

 Il deploy operativo verificato ha prodotto:

```
[WYP] service=WYP
[WYP] component=FDM
[WYP] version=1.0.0
[WYP] listening=http://0.0.0.0:10000
[WYP] HTTP backend ready
```

 Il servizio ha inoltre risposto correttamente a:

```
HEAD /
GET /
```

 con HTTP `200`.

 Il backend è quindi attualmente raggiungibile e avviabile in produzione.

---

 ## 40\. STRUTTURA CORE ATTUALE

 Il sottosistema `src/wyp/core/` contiene attualmente:

```
__init__.py
interpreter.py
kernel.py
llm.py
numeric.py
pipeline.py
problem.py
result.py
router.py
```

 Il core costituisce il livello di orchestrazione comune.

 Non deve contenere l'implementazione matematica specifica dei singoli domini.

---

 ## 41\. WYPProblem

 `core/problem.py` definisce la struttura canonica:

```
WYPProblem
```

 con:

```
intent
domain
problem
constraints
metadata
```

 La struttura permette di separare:

```
linguaggio naturale
    ->
rappresentazione strutturata
    ->
esecuzione
```

 `WYPProblem` non esegue matematica.

 È un contratto dati.

---

 ## 42\. INTERPRETER

 `core/interpreter.py` definisce il confine:

```
natural language
    ->
WYPProblem
```

 Sono presenti:

```
WYPInterpreter
StructuredProblemInterpreter
CallableInterpreter
interpret_mapping()
```

 L'interpreter non deve calcolare il risultato matematico.

 Un futuro adapter LLM può quindi essere collegato senza modificare il contratto del core.

---

 ## 43\. LLM BOUNDARY

 `core/llm.py` definisce il contratto LLM.

 L'architettura prevista è:

```
USER REQUEST
    ->
LLM interpretation
    ->
JSON strutturato
    ->
WYPProblem
    ->
deterministic solver
```

 e successivamente:

```
SolverResult
    ->
LLM response composer
    ->
risposta utente
```

 Il modello linguistico non è l'autorità matematica.

 Il risultato del solver rimane l'output autorevole.

 `llm.py` non è vincolato a:

```
OpenAI
GGUF
llama.cpp
transformers
altro provider
```

 Il runtime reale potrà essere aggiunto tramite adapter.

---

 ## 44\. SOLVER ROUTER

 `core/router.py` contiene:

```
WYPSolverRouter
```

 Il router associa:

```
domain + intent
    ->
solver
```

 Il router non implementa la matematica.

 Attualmente è presente l'adapter FDM:

```
fdm + compute
    ->
solve_fdm_problem

fdm + solve
    ->
solve_fdm_problem
```

 Il solver FDM esistente rimane quindi il proprietario dell'esecuzione FDM.

---

 ## 45\. EXECUTION PIPELINE

 `core/pipeline.py` definisce il flusso completo:

```
request
    ->
WYPInterpreter
    ->
WYPProblem
    ->
deterministic solver
    ->
SolverResult
    ->
WYPResponseLLM
    ->
final answer
```

 L'ordine è vincolante.

 ### Stage 1 — Interpretation

 Il testo dell'utente viene trasformato in `WYPProblem`.

 ### Stage 2 — Deterministic execution

 Il `WYPProblem` viene consegnato al solver appropriato.

 ### Stage 3 — Response composition

 Il `SolverResult` viene fornito al response composer.

 Il composer deve spiegare il risultato ricevuto.

 Non deve sostituirlo con un proprio calcolo.

---

 ## 46\. SOLVER RESULT

 `core/problem.py` contiene il contratto:

```
SolverResult
```

 Campi principali:

```
success
solver
value
answer
verification
warnings
metadata
```

 La proprietà fondamentale è:

```
value = risultato autorevole del solver
```

 `answer` è testo di presentazione opzionale.

 Il testo generato dall'LLM non può diventare automaticamente il risultato matematico.

---

 ## 47\. FDM

 Il dominio FDM rimane un sottosistema deterministico separato.

 Il router utilizza l'API pubblica FDM invece di duplicarne la matematica.

 Flusso:

```
WYPProblem(domain="fdm")
    ->
WYPSolverRouter
    ->
solve_fdm_problem()
    ->
WYP FDM API
    ->
SolverResult
```

 Questo mantiene separati:

```
interpretazione
routing
matematica FDM
composizione della risposta
```

---

 ## 48\. STATO LLM / GGUF

 Il contratto LLM è presente.

 L'integrazione di un modello locale GGUF **non è ancora da considerarsi completata**.

 La fase successiva consiste nell'aggiungere un adapter concreto che implementi:

```
WYPLLMBackend
```

 senza modificare:

```
WYPProblem
WYPInterpreter
WYPPipeline
WYPSolverRouter
SolverResult
```

 Il runtime potrà successivamente essere, ad esempio:

```
GGUF
    ->
llama.cpp / runtime compatibile
    ->
WYPLLMBackend
```

 Il modello deve essere considerato un componente di interpretazione/composizione, non il solver matematico autorevole.

---

 ## 49\. DOCUMENTI E FONTI ESTERNE

 L'architettura futura deve permettere al sistema di utilizzare materiale tecnico esterno quando necessario.

 Possibili sorgenti:

```
JSON
regole strutturate
Lean
LaTeX
PDF
documentazione tecnica
specifiche matematiche
moduli di calcolo
```

 Il flusso previsto è:

```
documento / fonte
    ->
ingestion
    ->
estrazione
    ->
normalizzazione
    ->
rappresentazione strutturata
    ->
modulo appropriato
```

 Il materiale estratto non deve essere automaticamente considerato vero.

 Deve essere distinto tra:

```
fonte
regola
definizione
formula
codice
teorema
risultato verificato
```

 La provenienza deve poter essere conservata nei metadata quando necessario.

---

 ## 50\. MULTI-MODULE SOLVING

 Il sistema dovrà poter comporre più moduli di calcolo quando una richiesta non appartiene a un singolo solver.

 Schema previsto:

```
user request
    ->
interpretation
    ->
problem decomposition
    ->
solver/module selection
    ->
module A
module B
module C
    ->
intermediate results
    ->
verification
    ->
final SolverResult
    ->
response composition
```

 Il router dovrà quindi evolvere da semplice dispatch:

```
domain + intent -> solver
```

 verso una possibile orchestrazione di più solver quando la struttura del problema lo richiede.

 Questa estensione non deve rompere l'attuale contratto FDM.

---

 ## 51\. OBIETTIVO FUNZIONALE

 L'obiettivo dell'architettura è che l'utente possa formulare direttamente una richiesta, ad esempio:

```
risolvi x o y
```

 oppure:

```
risolvi P vs NP
```

 senza dover conoscere quale modulo interno sia necessario.

 Il sistema deve determinare:

```
1. cosa sta chiedendo l'utente;
2. quale dominio è coinvolto;
3. quali dati sono necessari;
4. quali solver/moduli devono essere utilizzati;
5. quali verifiche sono disponibili;
6. come comporre il risultato finale.
```

 La capacità di interpretazione non deve però essere confusa con la capacità di dimostrazione.

 Se una richiesta richiede un teorema, una prova formale o una verifica che il sistema non possiede, il risultato deve dichiarare tale stato invece di inventare una soluzione.

---

 ## 52\. STATO OPERATIVO

 Stato attuale verificato:

```
PUBLIC INDEX
    -> ONLINE

WYP HTTP BACKEND
    -> ONLINE

FDM
    -> INTEGRATO

CORE PROBLEM CONTRACT
    -> PRESENTE

INTERPRETER CONTRACT
    -> PRESENTE

LLM CONTRACT
    -> PRESENTE

SOLVER ROUTER
    -> PRESENTE

EXECUTION PIPELINE
    -> PRESENTE

GGUF / LOCAL LLM RUNTIME
    -> NON ANCORA INTEGRATO

MULTI-SOLVER ORCHESTRATION
    -> PROSSIMO SVILUPPO

DOCUMENT / PDF / LEAN / LATEX INGESTION
    -> PROSSIMO SVILUPPO
```

---

 ## 53\. PROSSIMO PASSO

 Il prossimo sviluppo non consiste nel modificare nuovamente i contratti già presenti.

 Il passo successivo è implementare l'adapter LLM reale:

```
WYPLLMBackend
    ->
runtime locale / provider
    ->
WYPProblemLLM
    ->
WYPPipeline
```

 Successivamente dovrà essere collegato il router reale al pipeline applicativo, in modo che:

```
pagina pubblica
    ->
backend
    ->
LLM
    ->
WYPProblem
    ->
router
    ->
solver
    ->
SolverResult
    ->
LLM composer
    ->
risposta pubblica
```

 Questo è il punto di estensione previsto per trasformare l'attuale backend WYP/FDM in un sistema general-purpose multi-solver mantenendo il solver deterministico come autorità computazionale.

 Questa prosecuzione è allineata allo **stato effettivamente verificabile online**, inclusa la homepage pubblica e il fatto che il backend sia già operativo.  Auf2026
