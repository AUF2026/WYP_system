Ho letto **prima l'`AI_BOOTSTRAP.md` attuale**. È diventato obsoleto in diversi punti: continua a descrivere come “prossimo lavoro” cose che sono già state fatte, e soprattutto contiene il vecchio stato degli errori/import e una licenza di sviluppo che **non deve stare nel bootstrap pubblico**.  GitHub+1

 Questo è il bootstrap aggiornato allo stato attuale: **Render verde, Worker operativo, frontend pubblico passato al Worker, core `pipeline/router/llm` presenti, prossimo punto reale = verificare/chiudere il contratto `server.py /solve` end-to-end.**

 # AI BOOTSTRAP — WYP / AUF2026

 ## 0\. SCOPO

 Questo file è il punto ufficiale di ripresa del progetto per una nuova istanza AI.

 PRIMA DI MODIFICARE QUALSIASI FILE:

 1. leggere questo documento;
2. controllare la struttura reale della repository;
3. verificare il codice realmente presente;
4. non assumere che vecchie versioni del progetto siano ancora presenti;
5. non ricostruire componenti già esistenti;
6. non modificare componenti funzionanti senza una ragione verificata;
7. dopo ogni modifica eseguire almeno un controllo sintattico/import;
8. dopo modifiche al backend verificare il deploy Render;
9. dopo modifiche al gateway verificare Cloudflare;
10. infine verificare il percorso pubblico completo.

 Il progetto è:

 **WYP — AUF2026**

 Obiettivo:

 > fornire un'interfaccia pubblica per il sistema WYP mantenendo solver, matematica, verifica e licenze nella repository privata.

---

 # 1\. ARCHITETTURA ATTUALE

 Il percorso previsto è:

```
PUBLIC INTERNET
       |
       v
GitHub Pages
https://auf2026.github.io/WYP_system/
       |
       | HTML / CSS / JavaScript
       |
       v
Cloudflare Worker
https://wyp.auf2026.workers.dev/
       |
       | POST /solve
       v
AOS PRIVATE CORE
https://aos-private-core.onrender.com
       |
       v
Python WYP
       |
       +---- core
       +---- fdm
       +---- theorems
       +---- license
       |
       v
JSON RESULT
       |
       v
Cloudflare Worker
       |
       v
GitHub Pages
```

 Il browser pubblico NON deve chiamare direttamente Render.

 Il browser deve sempre utilizzare:

```
https://wyp.auf2026.workers.dev/solve
```

---

 # 2\. REPOSITORY PUBBLICA

 Repository:

```
AUF2026/WYP_system
```

 Homepage:

```
https://auf2026.github.io/WYP_system/
```

 La repository pubblica contiene solamente materiale destinato al pubblico.

 Può contenere:

```
index.html
about.html
research.html
documentation.html
license.html

assets/
css/
js/
images/
docs/
README.md
LICENSE.md
```

 NON deve contenere:

```
private keys
license signing keys
license tokens
Render secrets
Cloudflare credentials
private solver source
private theorem implementation
protected Lean source
private mathematical implementation
internal verification secrets
```

 Il JavaScript pubblico deve essere esclusivamente client-side UI + HTTP gateway client.

---

 # 3\. REPOSITORY PRIVATA

 Repository:

```
https://github.com/AUF2026/AOS-PRIVATE-CORE
```

 Questa è la repository del vero motore WYP.

 La matematica privata rimane qui.

 Struttura rilevante:

```
src/wyp/
    core/
    fdm/
    theorems/
    license/
    server.py
    ...
```

 Il frontend pubblico non deve duplicare queste strutture.

---

 # 4\. STATO RENDER — VERIFICATO

 Private core:

```
https://aos-private-core.onrender.com
```

 STATO ATTUALE:

```
ONLINE
```

 Ultimo deploy verificato:

```
Build successful 🎉
Deploying...
Setting WEB_CONCURRENCY=1
Running 'PYTHONPATH=src python -m wyp.server'

[WYP] service=WYP
[WYP] component=FDM
[WYP] version=1.0.0
[WYP] listening=http://0.0.0.0:10000
[WYP] HTTP backend ready
[WYP] 127.0.0.1 - "HEAD / HTTP/1.1" 200 -

Your service is live 🎉

[WYP] 127.0.0.1 - "GET / HTTP/1.1" 200 -
```

 Il processo Python parte correttamente.

 NON reinstallare FastAPI senza una necessità verificata.

---

 # 5\. RENDER BUILD

 Build command attuale:

```
pip install --upgrade pip && pip install -r src/wyp/requirements.txt
```

 Start command:

```
PYTHONPATH=src python -m wyp.server
```

 Python attualmente utilizzato da Render:

```
Python 3.14.3
```

 Dipendenze verificate nel deploy:

```
cryptography
cffi
pycparser
```

 Il deploy attuale funziona senza FastAPI.

---

 # 6\. CLOUDFLARE WORKER

 Gateway pubblico:

```
https://wyp.auf2026.workers.dev/
```

 Endpoint solver:

```
https://wyp.auf2026.workers.dev/solve
```

 Il Worker inoltra a:

```
https://aos-private-core.onrender.com/solve
```

 Il Worker attuale è un gateway HTTP.

 Responsabilità:

```
HTTP
CORS
JSON validation superficiale
proxy verso Render
ritorno della risposta upstream
timeout
gestione errori gateway
```

 Il Worker NON deve contenere:

```
private key
license key
license token
solver
FDM implementation
theorem implementation
Lean implementation
protected mathematics
private verification logic
```

 Il Worker non deve trasformarsi in un secondo backend matematico.

---

 # 7\. CLOUDFLARE STATUS

 Il Worker risponde alla root:

```
GET /
```

 con uno stato del gateway equivalente a:

```
{
  "status": "ONLINE",
  "service": "WYP",
  "gateway": "CLOUDFLARE"
}
```

 Questo endpoint indica che il gateway è raggiungibile.

 NON deve essere interpretato automaticamente come prova che il solver privato sia disponibile.

---

 # 8\. CLOUDFLARE /solve

 Endpoint:

```
POST https://wyp.auf2026.workers.dev/solve
```

 Il Worker accetta JSON.

 Il formato pubblico attuale è:

```
{
  "problem": "..."
}
```

 Il Worker inoltra il payload al private core senza introdurre parametri matematici propri.

 Esempio:

```
{
  "problem": "2 + 3"
}
```

 NON introdurre nel frontend:

```
modulus
dimension
quotient
FDM internals
```

 a meno che tali campi non diventino esplicitamente parte del contratto pubblico definitivo.

---

 # 9\. FRONTEND PUBBLICO — STATO ATTUALE

 Il JavaScript della homepage è stato aggiornato.

 Endpoint utilizzato dal browser:

```
const WYP_API =
    "https://wyp.auf2026.workers.dev/solve";
```

 Health/status:

```
const WYP_HEALTH =
    "https://wyp.auf2026.workers.dev/";
```

 Il browser NON chiama:

```
https://aos-private-core.onrender.com/solve
```

 direttamente.

 Il flusso è:

```
textarea
   |
   v
requestWYP()
   |
   v
Cloudflare Worker
   |
   v
Render private core
```

 Il frontend non contiene matematica.

---

 # 10\. FRONTEND — RESPONSABILITÀ

 Il JavaScript pubblico deve occuparsi esclusivamente di:

```
UI
input
button
keyboard shortcuts
HTTP
CORS-compatible requests
response parsing
status
error display
result display
```

 NON deve occuparsi di:

```
FDM mathematics
theorem proving
license verification
private keys
solver implementation
mathematical derivations
Lean execution
```

---

 # 11\. JOTFORM

 Il form contatti Jotform è indipendente dal solver.

 Il JavaScript WYP NON deve:

```
intercept Jotform submit
replace form.action
convert contact data into solver data
send contact data to Render
send contact data to Cloudflare /solve
```

 Il flusso della homepage rimane:

```
JOTFORM
   |
   | separato
   |
WYP TESTER
   |
   v
CLOUDFLARE
```

---

 # 12\. PRIVATE CORE — SERVER

 Il server è:

```
src/wyp/server.py
```

 Il server non deve contenere la matematica vera.

 Il server deve essere il boundary HTTP.

 Architettura:

```
HTTP request
     |
     v
request validation
     |
     v
license verification
     |
     v
WYP problem handling
     |
     v
deterministic solver
     |
     v
FDM / theorems / verification
     |
     v
JSON response
```

 La matematica rimane nei relativi moduli.

---

 # 13\. CORE — ARCHITETTURA ATTUALE

 Nella repository privata esistono ora componenti core per:

```
interpreter
problem
result
numeric
kernel
pipeline
router
llm
```

 Il principio architetturale è:

```
natural language
      |
      v
WYPProblem
      |
      v
deterministic solver
      |
      v
SolverResult
      |
      v
response composition
```

 L'LLM non è il solver matematico.

---

 # 14\. WYP PROBLEM

 Il problema canonico deve rappresentare una richiesta strutturata.

 Concettualmente:

```
{
  "intent": "solve",
  "domain": "fdm",
  "problem": {},
  "constraints": {},
  "metadata": {}
}
```

 Il formato reale deve essere determinato dal codice presente nella repository privata.

 NON inventare nuovi campi senza verificare:

```
src/wyp/core/problem.py
```

---

 # 15\. INTERPRETER

 Il componente interpreter ha il compito di trasformare una richiesta in:

```
WYPProblem
```

 Non deve eseguire direttamente la matematica.

 Principio:

```
interpretation != computation
```

 L'interpreter non deve essere utilizzato come sostituto del solver.

 Prima di aggiungere classi o funzioni all'interpreter:

```
controllare src/wyp/core/interpreter.py
```

 e controllare gli import effettivi in:

```
src/wyp/core/__init__.py
```

 IMPORTANTE:

 non aggiungere nomi esportati arbitrariamente.

 Gli errori precedenti:

```
ImportError:
StructuredProblemInterpreter

ImportError:
CallableInterpreter

ImportError:
interpret_mapping
```

 sono stati causati da disallineamenti tra gli export di `core/__init__.py` e le definizioni realmente presenti in `interpreter.py`.

 REGOLA:

 > prima verificare ciò che esiste, poi modificare gli export.

---

 # 16\. ROUTER

 Il router deterministico è:

```
src/wyp/core/router.py
```

 Responsabilità:

```
WYPProblem
     |
     v
domain + intent
     |
     v
registered deterministic solver
```

 Il router NON implementa matematica.

 Il router deve solo:

```
register
resolve
dispatch
```

 Il solver FDM esistente viene adattato al contratto WYP tramite il boundary previsto dal router.

 NON creare un secondo FDM engine nel router.

---

 # 17\. PIPELINE

 Il pipeline è:

```
request
   |
   v
interpreter
   |
   v
WYPProblem
   |
   v
deterministic solver
   |
   v
SolverResult
   |
   v
response composer
   |
   v
answer
```

 Il principio fondamentale è:

```
LLM = interpretation + response composition

Solver = authoritative computation
```

 Il composer non deve ricalcolare il risultato.

 Il risultato del solver è autorevole.

---

 # 18\. LLM BOUNDARY

 Il componente:

```
src/wyp/core/llm.py
```

 definisce il boundary astratto dell'LLM.

 Non deve introdurre direttamente:

```
OpenAI dependency
GGUF runtime
llama.cpp dependency
transformers dependency
specific inference provider
```

 Il core rimane indipendente dal provider.

 Il componente LLM può:

```
interpretare
comporre risposte
```

 ma non deve sostituire:

```
deterministic solver
verification
mathematical engine
```

---

 # 19\. FDM

 FDM rimane nel private core.

 Il modello interno FDM non deve diventare automaticamente il contratto pubblico.

 L'implementazione matematica rimane in:

```
src/wyp/fdm/
```

 Il kernel numerico deve rimanere separato dai layer:

```
HTTP
LLM
licensing
Cloudflare
Jotform
natural-language interpretation
```

---

 # 20\. AOS KERNEL

 L'AOSKernel è uno strato numerico.

 Concettualmente:

```
AOSKernel
   |
   +-- exact
   +-- decimal
   +-- float
   +-- power
   +-- identity
```

 NON deve conoscere:

```
HTTP
Cloudflare
Jotform
license
natural language
theorem registry
HTML
```

 Non modificare AOSKernel per risolvere problemi che appartengono al server/API.

---

 # 21\. THEOREMS

 I teoremi appartengono esclusivamente alla repository privata.

 Percorso:

```
src/wyp/theorems/
```

 Il frontend pubblico può descrivere:

```
formalization
verification
theorem proving
research
methodology
```

 ma non deve contenere le implementazioni private.

 Prima di modificare il theorem layer verificare i file realmente presenti.

 In particolare:

```
src/wyp/theorems/base.py
src/wyp/theorems/registry.py
src/wyp/theorems/__init__.py
```

 NON assumere che classi o funzioni citate in documentazione precedente esistano ancora.

---

 # 22\. LICENSING

 La verifica della licenza è SERVER-SIDE.

 Modulo:

```
src/wyp/license/
```

 La verifica utilizza Ed25519.

 Le credenziali/licenze effettive rimangono nelle variabili d'ambiente del private deployment.

 NON inserire mai in questo file:

```
license token
private signing key
secret credentials
Render secrets
Cloudflare secrets
```

 Il frontend non deve conoscere il token di licenza.

 Il Worker non deve conoscere il token di licenza.

 La verifica deve rimanere nel private core.

---

 # 23\. STATO ATTUALE DEL DEPLOY

 STATO VERIFICATO:

```
RENDER:
ONLINE

PYTHON SERVER:
ONLINE

WYP:
ONLINE

FDM:
LOADED

CLOUDFLARE WORKER:
ONLINE

PUBLIC HOMEPAGE:
CONFIGURATA PER USARE IL WORKER
```

 Il deploy Render attuale non presenta più:

```
SyntaxError in pipeline.py
IndentationError in pipeline.py
ImportError StructuredProblemInterpreter
ImportError CallableInterpreter
ImportError interpret_mapping
```

 Se questi errori ricompaiono, NON correggere aggiungendo casualmente simboli.

 Controllare prima:

```
core/__init__.py
core/interpreter.py
```

 e verificare che gli export corrispondano alle definizioni reali.

---

 # 24\. PROBLEMA ARCHITETTURALE ORIGINARIO

 Il vecchio endpoint FDM richiedeva parametri interni come:

```
{
  "modulus": 12,
  "dimension": 3,
  "name": "faure"
}
```

 mentre il frontend pubblico inviava:

```
{
  "problem": "2 + 3"
}
```

 Questo produceva errori del tipo:

```
Missing required field: modulus
```

 La soluzione NON è aggiungere `modulus` e `dimension` al frontend.

 La soluzione architetturale è:

```
public problem
      |
      v
WYP problem interpretation
      |
      v
deterministic routing
      |
      v
appropriate mathematical subsystem
      |
      v
verified result
```

 Il frontend non deve conoscere la struttura interna FDM.

---

 # 25\. CONTRATTO PUBBLICO ATTUALE

 Input:

```
POST /solve
Content-Type: application/json
```

 Body:

```
{
  "problem": "..."
}
```

 Gateway:

```
Cloudflare Worker
```

 Backend:

```
AOS PRIVATE CORE
```

 Il formato definitivo della risposta deve essere verificato in:

```
src/wyp/server.py
```

 e non inventato nel frontend.

---

 # 26\. PROSSIMO STEP REALE

 Il prossimo lavoro NON è più:

```
Render deployment
Cloudflare gateway
homepage endpoint
basic public JS
```

 Questi pezzi sono già configurati.

 Il prossimo step è:

```
PRIVATE CORE /solve
```

 e consiste nel verificare che il server riceva:

```
{
  "problem": "..."
}
```

 e lo trasformi correttamente nel nuovo flusso WYP.

 Target:

```
POST /solve
       |
       v
validate request
       |
       v
require_license()
       |
       v
problem interpretation
       |
       v
WYPProblem
       |
       v
router
       |
       v
deterministic solver
       |
       v
SolverResult
       |
       v
JSON
```

---

 # 27\. ORDINE DI VERIFICA

 Prima di modificare codice:

```
1. server.py
2. problem.py
3. interpreter.py
4. router.py
5. result.py
6. fdm/api.py
7. fdm/engine.py
8. theorem registry
9. verification
```

 Non modificare tutti i layer contemporaneamente.

---

 # 28\. TEST DA ESEGUIRE

 ## Test 1 — Render

```
GET /
```

 Atteso:

```
HTTP 200
```

 ## Test 2 — Worker

```
GET https://wyp.auf2026.workers.dev/
```

 Atteso:

```
{
  "status": "ONLINE",
  "service": "WYP",
  "gateway": "CLOUDFLARE"
}
```

 ## Test 3 — Private solve

 Testare direttamente:

```
POST https://aos-private-core.onrender.com/solve
```

 con il contratto reale definito da `server.py`.

 ## Test 4 — Worker solve

```
POST https://wyp.auf2026.workers.dev/solve
```

 con lo stesso payload.

 ## Test 5 — Public page

```
https://auf2026.github.io/WYP_system/
```

 e usare il tester.

---

 # 29\. TEST END-TO-END DEFINITIVO

 Il sistema è considerato correttamente integrato solo quando funziona:

```
Browser
   |
   v
GitHub Pages
   |
   v
WYP Public Tester
   |
   v
Cloudflare Worker
   |
   v
AOS Private Core
   |
   v
license verification
   |
   v
WYP problem
   |
   v
deterministic routing
   |
   v
FDM / Theorems / Verification
   |
   v
SolverResult
   |
   v
JSON
   |
   v
Cloudflare
   |
   v
Browser
```

---

 # 30\. REGOLE ASSOLUTE PER LA NUOVA ISTANZA AI

 NON:

```
reinstallare FastAPI senza necessità
spostare matematica nella repo pubblica
mettere licenze nel frontend
mettere secret nel Worker
chiamare Render direttamente dal browser
modificare Jotform per collegarlo al solver
aggiungere modulus/dimension al frontend per aggirare un errore
inventare classi mancanti
inventare import mancanti
duplicare il solver
duplicare FDM
duplicare i teoremi
far calcolare all'LLM il risultato matematico
```

 Prima di ogni modifica:

```
READ
VERIFY
MODIFY
IMPORT-CHECK
DEPLOY
TEST
```

---

 # 31\. REGOLA IMPORTANTE SUGLI EXPORT

 Gli errori recenti hanno mostrato un problema concreto:

```
core/__init__.py
```

 può esportare simboli che non esistono più in:

```
core/interpreter.py
```

 Esempi storici:

```
StructuredProblemInterpreter
CallableInterpreter
interpret_mapping
```

 REGOLA:

 > non aggiungere un nome a `__init__.py` perché sembra architetturalmente utile.

 Prima verificare:

```
hasattr(module, "Name")
```

 oppure leggere direttamente la definizione del file.

 Ogni `__all__` deve corrispondere a simboli realmente definiti/importabili.

---

 # 32\. REGOLA SUL BOOTSTRAP

 Questo documento descrive lo STATO ATTUALE.

 Quando un componente viene realmente completato:

```
aggiornare questo file
```

 e non lasciare istruzioni obsolete come se fossero ancora il prossimo step.

 In particolare aggiornare:

```
Render status
Worker status
public JS status
API contract
next step
known errors
repository structure
```

---

 # 33\. STATO DI RIPRESA CORRENTE

 Punto esatto da cui riprendere:

```
Render private core:
GREEN / ONLINE

Cloudflare Worker:
ONLINE

Public GitHub Pages:
CONFIGURATA PER PASSARE DAL WORKER

Public JS:
AGGIORNATO

Jotform:
SEPARATO DAL SOLVER

Core architecture:
INTERPRETER
PROBLEM
ROUTER
PIPELINE
LLM
RESULT
PRESENTI

FDM:
PRESENTE

AOSKernel:
PRESENTE

Licensing:
SERVER-SIDE

NEXT:
VERIFICARE E CHIUDERE IL CONTRATTO
PRIVATE CORE POST /solve
```

---

 # 34\. OBIETTIVO IMMEDIATO

 Non aggiungere altra architettura prima di avere verificato:

```
POST /solve
```

 Il singolo obiettivo è:

```
{
  "problem": "..."
}
```

 ↓

```
private core
```

 ↓

```
SolverResult
```

 ↓

```
JSON
```

 ↓

```
Worker
```

 ↓

```
Public tester
```

 Una volta verificato questo flusso, si può procedere con:

```
theorem discovery
verification
response composition
public documentation
About
Research
Documentation
License
```

---

 # 35\. PRINCIPIO FINALE

 WYP deve mantenere questa separazione:

```
PUBLIC
    |
    | problem
    v
CLOUDFLARE
    |
    | HTTP
    v
PRIVATE CORE
    |
    +-- license
    |
    +-- interpreter
    |
    +-- router
    |
    +-- solver
    |
    +-- FDM
    |
    +-- theorems
    |
    +-- verification
    |
    v
RESULT
```

 La repository pubblica mostra il sistema.

 La repository privata esegue il sistema.

 Il browser non deve conoscere la matematica privata.

 Il Worker non deve conoscere la matematica privata.

 Il solver deterministico rimane l'autorità sul risultato matematico.

 **Questo è lo stato da cui riprendere.**

 Questo sostituisce il vecchio bootstrap: ho anche eliminato dal documento il **token/licenza di sviluppo** che era presente nella versione pubblica attuale, perché non serve per riprendere il progetto e non va propagato in documentazione versionata.  GitHub
