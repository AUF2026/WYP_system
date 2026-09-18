# AI BOOTSTRAP — WYP / AUF2026

 ## 0\. SCOPO

 Questo file è il punto di ripresa operativo del progetto WYP per una nuova\
 istanza AI.

 Prima di modificare codice, leggere questo documento e verificare lo stato\
 reale del sistema.

 NON ripartire da zero.

 NON sostituire componenti funzionanti senza una ragione verificabile.

 NON modificare contemporaneamente più livelli dell'architettura senza\
 verificare ogni confine.

 Il progetto WYP appartiene all'ecosistema AUF2026 / AOS PRIVATE CORE.

 L'obiettivo è fornire un'interfaccia pubblica WYP utilizzabile attraverso\
 GitHub Pages mantenendo il motore matematico, il solver, la verifica delle\
 licenze e la logica protetta nell'ambiente privato.

---

 # 1\. ARCHITETTURA ATTUALE

 L'architettura di produzione è:

```
USER
  |
  v
GITHUB PAGES
PUBLIC WYP PAGE
  |
  +----------------------+
  |                      |
  v                      v
JOTFORM              WYP TESTER
CONTACT FORM              |
  |                       |
  v                       v
JOTFORM BACKEND     CLOUDFLARE WORKER
                          |
                          | HTTPS POST /solve
                          v
                   AOS PRIVATE CORE
                   RENDER
                          |
                          v
                     WYP / FDM
                          |
                          v
                DETERMINISTIC SOLVER
                          |
                          v
                    SOLVER RESULT
                          |
                          v
                   CLOUDFLARE WORKER
                          |
                          v
                     PUBLIC PAGE
```

 La separazione fondamentale è:

```
PUBLIC
   |
   v
GATEWAY
   |
   v
PRIVATE CORE
```

 Il browser NON deve chiamare direttamente il private core.

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

 La repository pubblica contiene esclusivamente materiale destinato al\
 browser e alla documentazione pubblica.

 Esempi:

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

 La repository pubblica deve essere considerata completamente osservabile.

 Qualunque codice JavaScript inserito nella pagina può essere letto\
 dall'utente.

 Di conseguenza il codice pubblico NON è un luogo adatto per conservare\
 segreti.

---

 # 3\. COSA NON DEVE ESSERE NELLA REPOSITORY PUBBLICA

 Non inserire:

```
private signing key
license token
Render credentials
Cloudflare credentials
API secrets
private solver implementation
protected mathematical implementation
private Lean source
protected theorem implementations
internal verification secrets
protected model weights
private mathematical derivations
```

 Il frontend pubblico deve rimanere un client HTTP e una UI.

---

 # 4\. REPOSITORY PRIVATA

 Repository privata:

```
AUF2026/AOS-PRIVATE-CORE
```

 Questa repository contiene il motore protetto.

 La matematica canonica e la logica di esecuzione devono rimanere nel\
 private core.

 Tra i componenti del private core:

```
src/wyp/
    core/
    fdm/
    theorems/
    license/
    server.py
    ...
```

 Il frontend pubblico NON deve duplicare queste strutture.

---

 # 5\. RENDER PRIVATE CORE

 URL del servizio:

```
https://aos-private-core.onrender.com
```

 Il deployment è attualmente funzionante.

 Runtime verificato:

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

 Il server attuale non utilizza FastAPI.

 NON reintrodurre FastAPI senza una necessità reale e senza verificare\
 nuovamente il deployment.

---

 # 6\. STATO DEL DEPLOYMENT RENDER

 Lo startup verificato è:

```
[WYP] service=WYP
[WYP] component=FDM
[WYP] version=1.0.0
[WYP] HTTP backend ready
```

 Il servizio è stato correttamente avviato da Render.

 Il processo utilizza la porta fornita dall'ambiente Render.

 Il deployment è quindi considerato operativo.

---

 # 7\. PRIVATE CORE HTTP

 Il private core espone HTTP.

 Endpoint principale:

```
GET /
```

 Endpoint solver:

```
POST /solve
```

 Il private core è il punto di esecuzione dell'applicazione WYP.

 Il contratto `/solve` deve essere orientato al problema WYP e non deve\
 esporre inutilmente al frontend i dettagli interni del modello FDM.

---

 # 8\. PRINCIPIO DEL CONTRATTO SOLVER

 Il frontend pubblico invia un problema.

 Esempio:

```
{
  "problem": "2 + 2"
}
```

 Il frontend NON deve trasformarsi in un'interfaccia diretta ai parametri\
 interni del solver.

 NON introdurre nel frontend parametri come:

```
modulus
dimension
quotient
base
```

 semplicemente perché tali valori possano essere utilizzati internamente.

 Se un parametro diventa parte del contratto pubblico, deve essere\
 esplicitamente definito dal private core.

---

 # 9\. CLOUDFLARE WORKER

 Worker pubblico:

```
https://wyp.auf2026.workers.dev/
```

 Endpoint solver:

```
https://wyp.auf2026.workers.dev/solve
```

 Il Worker è un gateway HTTP.

 Architettura:

```
Browser
    |
    v
Cloudflare Worker
    |
    v
AOS Private Core
    |
    v
WYP
```

 Il Worker NON è il solver.

---

 # 10\. RESPONSABILITÀ DEL WORKER

 Il Worker deve occuparsi di:

```
HTTP
CORS
request parsing
JSON syntax validation
request forwarding
upstream timeout
response forwarding
gateway status
```

 Il Worker NON deve contenere:

```
solver implementation
FDM implementation
theorem implementation
Lean implementation
protected mathematical logic
private signing key
license token
private verification secrets
```

 Il Worker non deve diventare un secondo private core.

---

 # 11\. WORKER STATUS

 Il Worker espone:

```
GET /
```

 Risposta attuale:

```
{
  "status": "ONLINE",
  "service": "WYP",
  "gateway": "CLOUDFLARE"
}
```

 Questo indica che il gateway pubblico è operativo.

 Non deve essere interpretato come prova indipendente della correttezza\
 matematica di un solver result.

 La verifica del solver avviene tramite:

```
POST /solve
```

---

 # 12\. WORKER /solve

 Il flusso è:

```
Browser
   |
   | POST /solve
   v
Cloudflare Worker
   |
   | POST /solve
   v
AOS Private Core
   |
   v
WYP / FDM
   |
   v
SolverResult
   |
   v
Cloudflare Worker
   |
   v
Browser
```

 Il Worker:

```
1. legge il body;
2. verifica che il body non sia vuoto;
3. verifica il JSON;
4. verifica che il JSON sia un object;
5. inoltra il payload;
6. applica il timeout;
7. restituisce la risposta del core.
```

 Il Worker non calcola il risultato matematico.

---

 # 13\. WORKER CONFIGURATION

 Endpoint configurato:

```
const PRIVATE_CORE_URL =
    "https://aos-private-core.onrender.com";
```

 Solver path:

```
/solve
```

 Timeout attuale:

```
30000 ms
```

 Il browser NON utilizza `PRIVATE_CORE_URL`.

 Il riferimento pubblico del browser è:

```
https://wyp.auf2026.workers.dev/solve
```

---

 # 14\. CORS

 Il Worker gestisce il CORS.

 Configurazione prevista:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization, Accept
```

 Il Worker gestisce anche:

```
OPTIONS /solve
```

 Il CORS è un meccanismo HTTP e non deve essere considerato un sistema di\
 autenticazione.

---

 # 15\. TIMEOUT E FALLBACK

 Il Worker utilizza un timeout upstream di:

```
30000 ms
```

 In caso di timeout:

```
{
  "status": "PRIVATE_CORE_TIMEOUT",
  "error": "..."
}
```

 In caso di impossibilità di raggiungere il core:

```
{
  "status": "PRIVATE_CORE_UNAVAILABLE",
  "error": "..."
}
```

 Il gateway non deve mai inventare un risultato matematico in caso di\
 errore upstream.

---

 # 16\. RISPOSTA DEL PRIVATE CORE

 Il Worker preserva la risposta del private core.

 Il principio è:

```
PRIVATE CORE RESULT
       |
       v
WORKER TRANSPORT
       |
       v
PUBLIC CLIENT
```

 Il Worker non modifica il significato matematico del risultato.

---

 # 17\. LICENSING

 Il licensing è server-side.

 Modulo:

```
wyp/license
```

 La verifica utilizza Ed25519.

 La configurazione privata viene mantenuta nell'ambiente del private core.

 Variabili previste:

```
WYP_LICENSE_KEY
WYP_LICENSE_PUBLIC_KEY
```

 La funzione di verifica è:

```
require_license()
```

 La verifica può comprendere:

```
token presence
token structure
Base64URL decoding
JSON parsing
Ed25519 signature verification
product verification
claims verification
issued_at
expires_at
expiration
```

 I valori effettivi delle credenziali NON devono essere riportati in questo\
 documento.

---

 # 18\. REGOLA SUI SEGRETI

 NON inserire nel:

```
frontend
Git
GitHub Pages
Cloudflare Worker source
```

 qualsiasi:

```
private key
license token
signing secret
Render credential
Cloudflare credential
API secret
```

 La configurazione segreta deve rimanere nell'ambiente appropriato.

---

 # 19\. PUBLIC VERIFICATION KEY

 Una public verification key è distinta dalla private signing key.

 La verifica della licenza rimane responsabilità del private core.

 Il browser non deve ricevere la chiave pubblica semplicemente perché è\
 tecnicamente pubblicabile.

 Non introdurre materiale crittografico nel frontend senza una necessità\
 architetturale documentata.

---

 # 20\. WYP / FDM

 Il private core contiene il sistema FDM.

 Componenti concettuali:

```
FDMModel
FDMDerivation
FDMComputation
FDMEngine
```

 Il core numerico include AOSKernel.

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

 AOSKernel NON deve conoscere:

```
HTTP
Cloudflare
JotForm
HTML
browser UI
natural-language UI
licensing workflow
```

 La separazione dei livelli deve essere mantenuta.

---

 # 21\. THEOREMS

 I teoremi appartengono al private core.

 Modulo:

```
wyp.theorems
```

 La parte pubblica può descrivere:

```
research
methodology
formalization
verification
theorems
FDM
solver
```

 La parte pubblica NON deve contenere:

```
private theorem implementations
private Lean source
internal registry logic
protected derivations
```

---

 # 22\. LLM BOUNDARY

 Regola architetturale fondamentale:

```
LLM != SOLVER
```

 Un LLM può essere utilizzato come componente di:

```
interpretation
classification
problem structuring
response composition
```

 Il modello linguistico non è l'autorità matematica.

 Il flusso previsto è:

```
USER TEXT
    |
    v
LLM / INTERPRETER
    |
    v
STRUCTURED WYP PROBLEM
    |
    v
DETERMINISTIC ROUTER
    |
    v
DETERMINISTIC SOLVER
    |
    v
SOLVER RESULT
    |
    v
RESPONSE COMPOSER
    |
    v
USER
```

 Il solver deterministico rimane l'autorità del risultato matematico.

---

 # 23\. STRUCTURED PROBLEM BOUNDARY

 Il testo naturale non deve essere trattato come risultato matematico.

 L'interpretazione deve produrre una struttura validabile:

```
WYPProblem
```

 Il confine è:

```
natural language
    |
    v
interpreter
    |
    v
WYPProblem
    |
    v
deterministic solver
```

 Il solver riceve una struttura validata e non un output libero non\
 controllato del modello linguistico.

---

 # 24\. RESPONSE COMPOSITION

 Il response composer può ricevere:

```
original request
authoritative SolverResult
optional context
```

 Il composer deve:

```
explain
format
contextualize
```

 Il composer NON deve:

```
invent numerical results
replace solver values
silently modify solver output
claim verification not present in SolverResult
```

 La distinzione tra:

```
exact
decimal
floating
verified
explanation
```

 deve essere mantenuta.

---

 # 25\. PUBLIC PAGE

 Homepage:

```
https://auf2026.github.io/WYP_system/
```

 La homepage è il punto di ingresso pubblico.

 La pagina contiene due flussi indipendenti:

```
JotForm
    |
    v
JotForm backend
```

 e:

```
WYP Tester
    |
    v
Cloudflare Worker
    |
    v
Private Core
```

 Questi flussi NON devono essere accoppiati.

---

 # 26\. JOTFORM

 Il form contatti è gestito da JotForm.

 JotForm rimane indipendente dal solver.

 Il JavaScript WYP NON deve:

```
intercettare arbitrariamente il submit JotForm
modificare form.action
sostituire il form
inviare dati del contatto al solver
inviare dati personali al private core
trasformare il submit in una richiesta WYP
```

 Il form deve continuare a funzionare secondo la configurazione JotForm\
 presente nella pagina.

---

 # 27\. PUBLIC WYP TESTER

 Il tester pubblico utilizza:

```
https://wyp.auf2026.workers.dev/solve
```

 Il browser NON deve chiamare direttamente:

```
https://aos-private-core.onrender.com/solve
```

 Il browser deve conoscere il Worker come endpoint pubblico.

---

 # 28\. PUBLIC JAVASCRIPT

 Il JavaScript pubblico è responsabile di:

```
UI
WYP tester
POST al Worker
visualizzazione risultato
gestione errori
health/status
keyboard shortcuts
```

 Il JavaScript pubblico NON deve contenere:

```
FDM equations
solver implementation
theorem implementation
license verification
license token
private key
Render credentials
private mathematical logic
```

 Il frontend deve rimanere un client HTTP.

---

 # 29\. PUBLIC API

 Il frontend può esporre:

```
window.WYP
```

 con wrapper come:

```
WYP.api
WYP.health
WYP.solve
```

 Può inoltre esporre:

```
window.solveWYP(...)
```

 Queste funzioni devono rimanere wrapper HTTP.

 Nessuna logica matematica deve essere trasferita nel browser.

---

 # 30\. PUBLIC RESPONSE STATES

 Il frontend deve distinguere almeno:

```
SUCCESS
LICENSE_REQUIRED
ENGINE_ERROR
INVALID_REQUEST
PRIVATE_CORE_UNAVAILABLE
PRIVATE_CORE_TIMEOUT
PRIVATE_CORE_INVALID_RESPONSE
METHOD_NOT_ALLOWED
NOT_FOUND
UNKNOWN STATUS
```

 Il frontend deve presentare il significato ricevuto dal backend senza\
 trasformarlo in una propria interpretazione matematica.

---

 # 31\. PUBLIC HEALTH

 Il frontend controlla:

```
https://wyp.auf2026.workers.dev/
```

 Il browser non deve interrogare direttamente Render per il normale status\
 della pagina pubblica.

---

 # 32\. MENU E PAGINE

 La struttura pubblica prevista è:

```
WYP
├── Home
├── About
├── Research
├── Documentation
└── License
```

 Pagine:

```
index.html
about.html
research.html
documentation.html
license.html
```

 Il progetto deve rimanere statico e semplice.

 Non introdurre framework o una SPA senza una necessità concreta.

---

 # 33\. CONTENUTO PUBBLICO

 La parte pubblica può descrivere:

```
WYP
AUF2026
research
methodology
mathematical approach
formalization
verification
FDM
theorems
Lean
solver
licensing
documentation
```

 Le dichiarazioni tecniche devono distinguere chiaramente tra:

```
implemented
tested
verified
formally verified
published
experimental
research claim
```

 Un risultato non deve essere descritto come formalmente verificato se tale\
 verifica non è effettivamente disponibile.

---

 # 34\. TEST END-TO-END

 Il test end-to-end è stato completato.

 La catena operativa verificata è:

```
PUBLIC PAGE
    |
    v
CLOUDFLARE WORKER
    |
    v
AOS PRIVATE CORE
    |
    v
WYP / FDM
    |
    v
RESPONSE
```

 Il Worker pubblico è raggiungibile.

 Il private core Render è operativo.

 Il gateway `/solve` è operativo.

 Il tester pubblico utilizza il Worker.

---

 # 35\. STATO ATTUALE DEL SISTEMA

 Componenti operativi:

```
Render deployment
Python runtime
private WYP server
FDM component
HTTP backend
Cloudflare Worker
Worker root status
Worker /solve gateway
CORS
upstream timeout
public WYP tester
public/private separation
JotForm separation
license infrastructure
Ed25519 verification infrastructure
end-to-end request path
```

 Stato Render verificato:

```
[WYP] service=WYP
[WYP] component=FDM
[WYP] version=1.0.0
[WYP] HTTP backend ready
```

 Stato Worker verificato:

```
{
  "status": "ONLINE",
  "service": "WYP",
  "gateway": "CLOUDFLARE"
}
```

 Il sistema non è più nella fase di configurazione iniziale del gateway.

---

 # 36\. ERRORI STORICI DA NON REINTRODURRE

 Durante lo sviluppo si sono verificati incompatibilità tra:

```
core/__init__.py
core/interpreter.py
```

 Sono comparsi errori come:

```
ImportError:
cannot import name 'StructuredProblemInterpreter'
```

```
ImportError:
cannot import name 'CallableInterpreter'
```

```
ImportError:
cannot import name 'interpret_mapping'
```

 Questi errori sono stati corretti riallineando gli import/export del core.

 REGOLA:

 Prima di aggiungere un import in `__init__.py`, verificare che il simbolo\
 esista realmente nel modulo destinazione.

 NON creare classi, alias o funzioni inesistenti per soddisfare un import.

 NON modificare contemporaneamente molti moduli senza testare l'import chain.

---

 # 37\. REGOLA DI STABILITÀ

 Quando un componente è verificato come funzionante:

```
NON riscriverlo senza necessità.
```

 Prima di modificare un livello:

```
1. identificare il problema;
2. verificare il contratto;
3. modificare il minimo necessario;
4. eseguire il test del livello;
5. eseguire il test end-to-end.
```

 Non correggere un errore frontend modificando arbitrariamente il solver.

 Non correggere un errore Worker spostando la matematica nel Worker.

 Non correggere un errore di contratto esponendo dettagli interni FDM al\
 browser.

---

 # 38\. SEPARAZIONE DEI TRE LIVELLI

 Il sistema ha tre livelli:

```
PUBLIC
    GitHub Pages
        |
        v
GATEWAY
    Cloudflare Worker
        |
        v
PRIVATE
    AOS Private Core
```

 Regola:

```
Browser -> Cloudflare -> Render
```

 NON:

```
Browser -> Render
```

 NON:

```
Browser -> private solver
```

 SÌ:

```
Browser -> public API gateway -> private solver
```

---

 # 39. CLOUDFLARE NON È IL SOLVER

 Non spostare nel Worker:

```
FDM
theorems
AOSKernel
Lean
license verification
protected mathematics
```

 Il Worker è:

```
HTTP gateway
```

 L'eventuale introduzione futura di:

```
Cloudflare AI
Workers AI
Llama
altri LLM
```

 non modifica automaticamente l'architettura.

 Qualunque modello futuro deve avere un ruolo esplicitamente definito.

---

 # 40\. PROSSIMO SVILUPPO

 Il sistema di trasporto è operativo.

 I prossimi interventi devono concentrarsi sul livello applicativo, non sul\
 rifacimento della catena di deployment già funzionante.

 Ordine consigliato:

```
1. stabilizzazione del contratto WYPProblem;
2. stabilizzazione del SolverResult;
3. integrazione controllata dell'interpreter;
4. routing deterministico;
5. solver specifici;
6. response composition;
7. test automatici;
8. documentazione pubblica;
9. rifinitura UI.
```

 Il gateway non deve essere modificato per risolvere problemi appartenenti\
 a questi livelli.

---

 # 41\. PRINCIPIO FONDAMENTALE

 L'architettura WYP deve mantenere questa separazione:

```
INTERPRETATION
      |
      v
STRUCTURED PROBLEM
      |
      v
DETERMINISTIC COMPUTATION
      |
      v
VERIFIED / AUTHORITATIVE RESULT
      |
      v
RESPONSE COMPOSITION
```

 Il modello linguistico può interpretare e spiegare.

 Il solver deterministico esegue il calcolo.

 Il private core rimane il confine di protezione.

 Il Cloudflare Worker trasporta.

 La pagina pubblica presenta.

 JotForm rimane indipendente.

---

 # 42\. REGOLE OPERATIVE PER UNA NUOVA ISTANZA AI

 Una nuova istanza AI deve:

```
1. leggere questo file;
2. verificare lo stato reale prima di modificare codice;
3. non assumere che un vecchio errore sia ancora presente;
4. non reintrodurre FastAPI senza necessità;
5. non collegare il browser direttamente a Render;
6. non mettere segreti nella repository pubblica;
7. non intercettare il submit JotForm;
8. non trasferire la matematica nel Worker;
9. non trasferire la matematica nel browser;
10. non usare un LLM come autorità matematica quando esiste un
    SolverResult deterministico;
11. verificare gli import prima di modificarli;
12. mantenere separati PUBLIC, GATEWAY e PRIVATE;
13. testare ogni modifica prima di procedere al livello successivo.
```

---

 # 43\. STATO DI RIPRESA

 STATO:

```
PRODUCTION TRANSPORT PATH OPERATIONAL
```

 PUBLIC:

```
GitHub Pages
WYP public tester
JotForm
```

 GATEWAY:

```
Cloudflare Worker
GET /
POST /solve
CORS
timeout
response forwarding
```

 PRIVATE:

```
Render
WYP
FDM
licensing
deterministic execution
```

 ARCHITECTURE:

```
PUBLIC -> CLOUDFLARE -> PRIVATE CORE
```

 LLM:

```
interpretation / response composition only
```

 SOLVER:

```
deterministic and authoritative
```

 NEXT FOCUS:

```
WYP structured problem contract
deterministic routing
solver integration
result contract
automated verification
public documentation
```

 NON-NEGOTIABLE:

```
DO NOT BREAK THE WORKING TRANSPORT ARCHITECTURE
DO NOT EXPOSE THE PRIVATE CORE TO THE BROWSER
DO NOT PUT SECRETS IN THE PUBLIC REPOSITORY
DO NOT TURN CLOUDFLARE INTO THE SOLVER
DO NOT TURN THE LLM INTO THE MATHEMATICAL AUTHORITY
DO NOT COUPLE JOTFORM TO WYP
```

```

Questa è la versione da usare come nuovo riferimento: il documento attuale del repository contiene ancora la vecchia fase di “prossimo lavoro” e i test 30–35 come se fossero da eseguire; ora vanno trattati come **completati**.  github.com
```
