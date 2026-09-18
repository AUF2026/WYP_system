Ho letto il `AI_BOOTSTRAP.md` attuale direttamente dalla repository pubblica.  GitHub+1

 Lo aggiorno tenendo conto dei progressi **effettivamente raggiunti**: gli 8 moduli che abbiamo completato, `server.py` corretto, deploy Render riuscito e server avviato su Python 3.14.3. Non segno invece come completato il nuovo contratto `/solve` problema→teorema→FDM, perché quello è il prossimo lavoro.  GitHub

 Sostituisci `docs/AI_BOOTSTRAP.md` con questo:

 AI BOOTSTRAP — WYP / AUF2026

# AI BOOTSTRAP — WYP / AUF2026

 ## 0\. SCOPO

 Questo file è il punto ufficiale di ripresa del progetto per una nuova istanza AI.

 Una nuova istanza deve:

 1. leggere questo file prima di modificare il codice;
2. verificare lo stato reale della repository;
3. rispettare i componenti già completati;
4. non ripartire da zero;
5. non reintrodurre problemi già risolti;
6. procedere un componente alla volta;
7. mantenere aggiornata questa documentazione dopo ogni milestone verificata.

 Il progetto è WYP, nell'ecosistema AUF2026 / AOS-PRIVATE-CORE.

 Obiettivo architetturale:

 > fornire un sistema WYP pubblico attraverso GitHub Pages, mantenendo matematica, solver, teoremi, verifica e licensing nel private core.

---

 # 1\. ARCHITETTURA

 L'architettura prevista è:

```
PUBLIC INTERNET
      |
      v
GitHub Pages
AUF2026/WYP_system
      |
      v
Public WYP Tester
      |
      v
Cloudflare Worker
wyp.auf2026.workers.dev
      |
      v
Private WYP Core
AOS-PRIVATE-CORE
Render
      |
      +------------------+
      |                  |
      v                  v
   THEOREMS             FDM
      |                  |
      +--------+---------+
               |
               v
          NUMERICAL CORE
               |
               v
        VERIFICATION
               |
               v
          JSON RESULT
```

 Il browser pubblico non deve contenere la matematica privata.

 Il Cloudflare Worker deve rimanere un gateway.

 Il private core rimane l'autorità per:

 - matematica;
- teoremi;
- FDM;
- numerical kernel;
- verifica;
- licensing;
- solver.

---

 # 2\. REPOSITORY PUBBLICA

 Repository:

```
https://github.com/AUF2026/WYP_system
```

 GitHub Pages:

```
https://auf2026.github.io/WYP_system/
```

 La repository pubblica può contenere:

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

 Non deve contenere:

 - private key;
- signing key;
- license token;
- Render secrets;
- Cloudflare credentials;
- solver privato;
- implementazioni matematiche protette;
- sorgenti Lean privati;
- teoremi privati;
- copie della logica interna del solver.

 Il JavaScript pubblico deve essere solamente un client del gateway.

---

 # 3\. REPOSITORY PRIVATA

 Repository:

```
https://github.com/AUF2026/AOS-PRIVATE-CORE
```

 Questa repository contiene il motore WYP.

 Struttura principale:

```
src/wyp/
    core/
    fdm/
    theorems/
    license/
    server.py
```

 La matematica privata rimane qui.

 In particolare:

```
wyp.core
wyp.fdm
wyp.theorems
wyp.license
server
```

 La repository pubblica non deve duplicare questi componenti.

---

 # 4\. STATO CORRENTE DEL PRIVATE CORE

 ## COMPLETATO E VERIFICATO

 I seguenti componenti sono completati:

```
src/wyp/theorems/base.py
src/wyp/theorems/registry.py
src/wyp/theorems/__init__.py

src/wyp/fdm/engine.py
src/wyp/fdm/model.py
src/wyp/fdm/verification.py

src/wyp/core/numeric.py
src/wyp/core/result.py

src/wyp/server.py
```

 Stato:

```
8 / 8 componenti completati
```

 Questi componenti costituiscono il baseline corrente.

 Non devono essere riscritti da zero senza una necessità verificata.

---

 # 5\. FDM MODEL

 Il modello FDM canonico è:

```
M_d(U) = Q(U)^d
```

 Le strutture principali sono:

```
FDMModel
FDMDerivation
FDMComputation
```

 `FDMModel` rappresenta la specifica matematica.

 `FDMDerivation` conserva la derivazione strutturale.

 `FDMComputation` rappresenta il risultato dell'esecuzione.

 Il modello non deve contenere HTTP, licensing o logica web.

---

 # 6\. FDM ENGINE

 Il componente:

```
src/wyp/fdm/engine.py
```

 è il livello di esecuzione del modello FDM.

 Responsabilità:

```
FDMModel
    |
    v
FDMEngine
    |
    v
numerical kernel
    |
    v
FDMComputation
```

 La relazione canonica eseguita è:

```
M_d(U) = Q(U)^d
```

 Il motore supporta i domini numerici previsti:

```
exact
decimal
float
```

 Il motore non deve duplicare la logica numerica del kernel.

---

 # 7\. NUMERICAL CORE

 Il livello numerico è separato dalla matematica FDM.

 Il componente:

```
src/wyp/core/numeric.py
```

 gestisce conversione e aritmetica numerica.

 Rappresentazioni:

```
exact
decimal
float
```

 Il kernel numerico deve rimanere indipendente da:

 - HTTP;
- Cloudflare;
- licensing;
- linguaggio naturale;
- UI;
- Jotform;
- teoremi.

 La separazione architetturale è intenzionale.

---

 # 8\. RESULT LAYER

 Il componente:

```
src/wyp/core/result.py
```

 fornisce strutture risultato condivise:

```
NumericResult
VerificationCheck
VerificationResult
ExecutionResult
```

 Il valore numerico contenuto nel risultato rimane autorevole.

 La serializzazione è solamente una rappresentazione per API/JSON.

 Non deve alterare il valore numerico interno.

---

 # 9\. FDM VERIFICATION

 Il componente:

```
src/wyp/fdm/verification.py
```

 fornisce verifica indipendente del modello FDM.

 La verifica ricostruisce indipendentemente:

```
Q^d
```

 e confronta il risultato con la computazione.

 La verifica deve rimanere separata dall'esecuzione.

 Flusso:

```
FDMModel
    |
    +--> FDMEngine
    |
    +--> independent verification
```

 Questo evita che il verifier diventi semplicemente una copia dell'engine.

---

 # 10\. THEOREMS

 Il sottosistema:

```
src/wyp/theorems/
```

 è completato nella sua struttura iniziale.

 Componenti:

```
base.py
registry.py
__init__.py
```

 Il theorem registry deve diventare il punto di ingresso per la futura trasformazione:

```
problema
    |
    v
theorem discovery
    |
    v
teorema applicabile
    |
    v
modello matematico
    |
    v
FDM / numerical engine
    |
    v
verification
```

 Questo passaggio non è ancora considerato completato.

---

 # 11\. SERVER

 Il server:

```
src/wyp/server.py
```

 è stato rifatto come server HTTP standard-library.

 Non usa FastAPI.

 Il comando di avvio verificato è:

```
PYTHONPATH=src python -m wyp.server
```

 Il server utilizza:

```
http.server
ThreadingHTTPServer
BaseHTTPRequestHandler
```

 Endpoint presenti:

```
GET /
HEAD /
GET /health
POST /solve
OPTIONS
```

 Il server gestisce:

```
HTTP
    |
    v
request validation
    |
    v
license verification
    |
    v
FDM processing
    |
    v
JSON response
```

 Il server non deve diventare il luogo dove duplicare la matematica privata.

---

 # 12\. RENDER DEPLOY

 Il private core è deployato su Render:

```
https://aos-private-core.onrender.com
```

 Il deploy è stato verificato come riuscito.

 Ambiente verificato:

```
Python 3.14.3
```

 Build command:

```
pip install --upgrade pip && pip install -r src/wyp/requirements.txt
```

 Start command:

```
PYTHONPATH=src python -m wyp.server
```

 Il server si avvia sulla porta fornita da Render.

 Il log verificato include:

```
[WYP] service=WYP
[WYP] component=FDM
[WYP] HTTP backend ready
```

 Il servizio è quindi considerato:

```
RENDER DEPLOYMENT = GREEN
```

---

 # 13\. FASTAPI

 FastAPI NON è necessario per l'attuale server.

 La precedente dipendenza FastAPI è stata rimossa.

 Non reintrodurre FastAPI automaticamente.

 Prima di aggiungere una dipendenza HTTP:

 1. verificare la necessità;
2. verificare l'impatto sul deploy;
3. verificare il contratto architetturale;
4. evitare di modificare il server standard-library senza motivo.

---

 # 14\. LICENSING

 Il licensing è server-side.

 Modulo:

```
wyp.license
```

 La verifica utilizza Ed25519.

 Il private signing key non deve essere presente nella repository.

 Configurazione server-side:

```
WYP_LICENSE_KEY
WYP_LICENSE_PUBLIC_KEY
```

 La funzione principale è:

```
require_license()
```

 La licenza viene verificata prima dell'esecuzione protetta.

 Non mettere mai nel frontend:

 - license token;
- signing key;
- Render secret;
- credenziali private.

---

 # 15\. CLOUDFLARE WORKER

 Worker pubblico:

```
https://wyp.auf2026.workers.dev/
```

 Il Worker deve rimanere un gateway.

 Architettura:

```
Browser
   |
   v
Cloudflare Worker
   |
   v
AOS-PRIVATE-CORE
```

 Il Worker non deve contenere:

 - solver;
- matematica;
- FDM implementation;
- teoremi privati;
- Lean;
- private key;
- license token;
- Render secrets.

 Il Worker deve:

 1. ricevere HTTP;
2. gestire CORS;
3. validare superficialmente il JSON;
4. inoltrare la richiesta;
5. restituire la risposta.

---

 # 16\. PUBLIC SOLVER

 Il browser pubblico non deve chiamare direttamente:

```
https://aos-private-core.onrender.com
```

 Il browser deve chiamare:

```
https://wyp.auf2026.workers.dev/solve
```

 Il flusso corretto è:

```
USER
 |
 v
PUBLIC WYP TESTER
 |
 v
CLOUDFLARE WORKER
 |
 v
PRIVATE CORE
 |
 v
THEOREMS
 |
 v
FDM ENGINE
 |
 v
NUMERICAL CORE
 |
 v
VERIFICATION
 |
 v
RESULT
```

---

 # 17\. ATTUALE PROBLEMA API

 Il precedente `/solve` era orientato direttamente al modello FDM.

 Richiedeva campi come:

```
{
  "modulus": 12,
  "dimension": 3,
  "name": "faure"
}
```

 Questo è utile per testare direttamente FDM, ma non rappresenta ancora il contratto definitivo del WYP Solver pubblico.

 Il tester pubblico deve poter inviare un problema.

 Esempio:

```
{
  "problem": "2 + 3"
}
```

 oppure:

```
{
  "problem": "Dimostra che ...",
  "mode": "exact"
}
```

 Il formato definitivo deve essere stabilito dal private core.

 Il frontend NON deve inventare:

```
modulus
dimension
quotient
```

 solo per adattarsi all'implementazione interna.

---

 # 18\. NUOVO SOLVER CONTRACT

 Il prossimo obiettivo architetturale è:

```
POST /solve
```

 con un input orientato al problema.

 Pipeline prevista:

```
POST /solve
      |
      v
require_license()
      |
      v
problem parser
      |
      v
theorem registry
      |
      v
mathematical model
      |
      v
FDMEngine / numerical kernel
      |
      v
independent verification
      |
      v
structured result
```

 Questo è il prossimo grande passaggio.

 Non è ancora da considerarsi completato.

---

 # 19\. PUBLIC JAVASCRIPT

 Il JavaScript pubblico deve:

 - gestire la UI;
- raccogliere il problema;
- inviare il POST al Worker;
- mostrare il risultato;
- gestire gli errori;
- eventualmente mostrare lo stato del servizio.

 Non deve contenere:

```
FDM equations
solver logic
theorem implementation
license verification
license token
private key
Render secrets
```

 Non deve implementare matematica.

---

 # 20\. JOTFORM

 Jotform è separato dal solver.

 Il form contatti non deve essere trasformato in una richiesta `/solve`.

 Architettura:

```
Jotform
   |
   | indipendente
   |
WYP Solver
   |
   v
Cloudflare
```

 Il comportamento del form deve rimanere invariato salvo esplicita necessità.

---

 # 21\. PUBLIC PAGES

 La repository pubblica prevede:

```
Home
About
Research
Documentation
License
```

 File possibili:

```
index.html
about.html
research.html
documentation.html
license.html
```

 Il sito deve rimanere semplice e statico.

 Non introdurre framework inutili.

---

 # 22\. STATO ATTUALE

 ## COMPLETATO

```
☑ theorems/base.py
☑ theorems/registry.py
☑ theorems/__init__.py

☑ fdm/engine.py
☑ fdm/model.py
☑ fdm/verification.py

☑ core/numeric.py
☑ core/result.py

☑ server.py

☑ Render build
☑ Render deploy
☑ Python 3.14.3
☑ server HTTP standard-library
☑ GET /
☑ HEAD /
☑ /health
☑ POST /solve
☑ licensing server-side
☑ separazione public/private
```

 ## DA FARE

```
⬜ problem parser
⬜ theorem discovery
⬜ collegamento problem -> theorem registry
⬜ collegamento theorem -> mathematical model
⬜ nuovo contratto pubblico /solve
⬜ verifica end-to-end del nuovo /solve
⬜ allineamento Cloudflare Worker al nuovo contratto
⬜ aggiornamento public JavaScript
⬜ aggiornamento public tester
⬜ test completo Browser -> Worker -> Render -> Engine -> Verification
```

---

 # 23\. ORDINE DI LAVORO

 Procedere esclusivamente in questo ordine:

 ## Step 1 — Problem parser

 Creare il livello che riceve:

```
{
  "problem": "..."
}
```

 e costruisce una rappresentazione interna del problema.

 ## Step 2 — Theorem discovery

 Collegare il problema al:

```
theorems/registry.py
```

 senza duplicare i teoremi nel server.

 ## Step 3 — Mathematical model

 Trasformare il problema riconosciuto in un modello matematico interno.

 ## Step 4 — FDM execution

 Utilizzare:

```
FDMEngine
```

 e il numerical kernel già presente.

 ## Step 5 — Independent verification

 Utilizzare:

```
fdm/verification.py
```

 e/o:

```
core/result.py
```

 per produrre una verifica strutturata.

 ## Step 6 — API result

 Restituire JSON strutturato.

 ## Step 7 — Direct Render test

 Testare:

```
client
  |
  v
Render /solve
```

 prima di modificare il frontend.

 ## Step 8 — Cloudflare

 Testare:

```
client
  |
  v
Cloudflare
  |
  v
Render
```

 ## Step 9 — Public JS

 Solo dopo la verifica backend, aggiornare il tester pubblico.

 ## Step 10 — End-to-end

 Verificare:

```
GitHub Pages
    |
    v
WYP Tester
    |
    v
Cloudflare Worker
    |
    v
Private Core
    |
    v
License
    |
    v
Problem Parser
    |
    v
Theorem Registry
    |
    v
Mathematical Model
    |
    v
FDM / Numerical Core
    |
    v
Verification
    |
    v
JSON
    |
    v
Browser
```

---

 # 24\. REGOLE PER LA NUOVA ISTANZA AI

 Prima di modificare codice:

 1. leggere `docs/AI_BOOTSTRAP.md`;
2. controllare la repository reale;
3. controllare i file già completati;
4. non ripartire da zero;
5. non modificare componenti verificati senza motivo;
6. non reintrodurre FastAPI;
7. non spostare matematica privata nella repository pubblica;
8. non mettere licenze o segreti nel frontend;
9. non mettere private key in Git;
10. non far chiamare Render direttamente dal browser;
11. usare Cloudflare Worker come gateway;
12. non confondere Jotform con il solver;
13. non esporre strutture FDM interne come contratto pubblico senza necessità;
14. modificare prima il backend;
15. testare il backend prima del frontend;
16. dopo ogni milestone verificata aggiornare questo file;
17. procedere in parti quando un file è grande, evitando sostituzioni corrotte;
18. non dichiarare completato un componente finché non è stato effettivamente verificato.

---

 # 25\. REGOLA DI CONTINUITÀ

 Questo file deve essere aggiornato durante lo sviluppo.

 Ogni nuova istanza AI deve poter capire immediatamente:

```
cosa è completato
cosa è verificato
cosa è in corso
cosa è ancora da fare
qual è il prossimo singolo passaggio
```

 Non usare questo documento come semplice descrizione storica.

 È il registro operativo del progetto.

---

 # 26\. PUNTO ESATTO DI RIPRESA

 Stato attuale:

```
PRIVATE CORE
     |
     +-- THEOREMS          READY
     |
     +-- FDM MODEL         READY
     |
     +-- FDM ENGINE        READY
     |
     +-- FDM VERIFICATION  READY
     |
     +-- NUMERIC CORE      READY
     |
     +-- RESULT LAYER      READY
     |
     +-- SERVER            READY
     |
     +-- RENDER            GREEN
```

 Il prossimo punto da implementare è:

```
PROBLEM INPUT
     |
     v
PROBLEM PARSER
     |
     v
THEOREM REGISTRY
     |
     v
MATHEMATICAL MODEL
     |
     v
FDM ENGINE
     |
     v
VERIFICATION
     |
     v
STRUCTURED RESPONSE
```

 Non ripartire dal deploy Render.

 Non modificare il numerical core senza necessità.

 Non riscrivere FDM.

 Non riscrivere il theorem subsystem già completato.

 Il prossimo obiettivo concreto è:

```
PRIVATE CORE /solve
        ↓
problem-oriented request
        ↓
theorem discovery
        ↓
mathematical execution
        ↓
independent verification
        ↓
structured JSON
```

 Solo dopo:

```
CLOUDFLARE /solve
        ↓
PUBLIC WYP TESTER
```

 e infine:

```
FULL END-TO-END TEST
```

---

 # 27\. BASELINE

 Baseline corrente:

```
WYP / AUF2026
Private Core: AOS-PRIVATE-CORE
Public Repo: WYP_system

FDM subsystem: COMPLETE
Theorem subsystem: COMPLETE
Numerical/result layer: COMPLETE
HTTP server: COMPLETE
Render deployment: VERIFIED
Public solver contract: NEXT
```

 Questo è il punto ufficiale da cui la prossima istanza AI deve continuare.

 Questo sostituisce il bootstrap precedente e soprattutto **toglie l'ambiguità tra ciò che era previsto e ciò che abbiamo realmente completato**. Il prossimo lavoro rimane quindi chiaramente il `problem parser → theorem registry → model → execution → verification`, senza toccare inutilmente ciò che è già verde.
