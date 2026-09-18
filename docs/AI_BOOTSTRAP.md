Ho letto **l'intero `AI_BOOTSTRAP.md` attuale** della repo pubblica, compresa la parte finale aggiunta sullo stato del backend.  GitHub+1

 Ci sono però alcune informazioni ormai superate rispetto allo stato che mi hai appena mostrato: soprattutto **Render è già verde**, il server parte con `PYTHONPATH=src python -m wyp.server`, il Worker è operativo come gateway e il JS pubblico è già stato riallineato al Worker. Quindi il bootstrap va riscritto per fotografare **lo stato reale attuale**, senza lasciare istruzioni vecchie come "definire il vero `/solve`" se quello è già stato implementato.  GitHub

 Ti lascio quindi il file completo aggiornato, pronto da sostituire a `docs/AI_BOOTSTRAP.md`.

 # AI BOOTSTRAP — WYP / AUF2026

 ## 0\. SCOPO DI QUESTO FILE

 Questo file è il punto di ripresa operativo del progetto per una nuova istanza AI.

 Una nuova istanza deve leggere questo file **prima di modificare codice**.

 NON ripartire da zero.

 NON ricostruire l'architettura senza prima verificare lo stato reale della repository.

 NON sostituire componenti funzionanti senza una ragione tecnica verificata.

 Il progetto è **WYP**, parte dell'ecosistema **AUF2026 / AOS-PRIVATE-CORE**.

 Obiettivo:

 > mantenere un sistema WYP pubblico, accessibile tramite GitHub Pages, con un frontend semplice e pubblico, mentre matematica, solver, teoremi, verifica e licensing rimangono nel private core.

 L'architettura è deliberatamente separata:

```
PUBLIC WEB
    |
    v
GitHub Pages
    |
    +--------------------+
    |                    |
    v                    v
Jotform             WYP Tester
                         |
                         v
                Cloudflare Worker
                         |
                         v
                AOS PRIVATE CORE
                    Render
                         |
                         v
                    WYP / FDM
```

---

 # 1\. STATO ATTUALE

 Lo stato attuale verificato è:

```
GitHub Pages
    |
    v
Cloudflare Worker
    |
    v
AOS Private Core
    |
    v
WYP server
    |
    v
FDM / WYP
```

 Il private core Render è attualmente operativo.

 Deploy verificato:

```
==> Build successful 🎉
==> Deploying...
[WYP] service=WYP
[WYP] component=FDM
[WYP] version=1.0.0
[WYP] listening=http://0.0.0.0:10000
[WYP] HTTP backend ready
[WYP] 127.0.0.1 - "HEAD / HTTP/1.1" 200 -
==> Your service is live 🎉
```

 URL:

```
https://aos-private-core.onrender.com
```

 Il Worker pubblico è operativo:

```
https://wyp.auf2026.workers.dev/
```

 Endpoint solver pubblico:

```
https://wyp.auf2026.workers.dev/solve
```

 La pagina pubblica è:

```
https://auf2026.github.io/WYP_system/
```

---

 # 2\. REPOSITORY PUBBLICA

 Repository:

```
AUF2026/WYP_system
```

 URL:

```
https://github.com/AUF2026/WYP_system
```

 GitHub Pages:

```
https://auf2026.github.io/WYP_system/
```

 La repository è PUBBLICA.

 Deve contenere solamente materiale destinato al frontend/documentazione pubblica.

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

 La repository pubblica NON deve contenere:

```
private keys
license signing keys
license tokens
Render secrets
Cloudflare credentials
private solver source
protected mathematical implementation
protected Lean source
private theorem implementation
internal verification logic
private backend credentials
```

 Il JavaScript pubblico deve comportarsi come un client HTTP.

 Non deve implementare la matematica privata.

---

 # 3\. REPOSITORY PRIVATA

 Repository:

```
AUF2026/AOS-PRIVATE-CORE
```

 Il private core contiene il motore WYP.

 La matematica canonica deve rimanere nel private core.

 Struttura concettuale:

```
src/wyp/

    core/

    fdm/

    theorems/

    license/

    server.py

    ...
```

 Il private core è il luogo corretto per:

```
WYP solver
FDM
AOSKernel
theorems
verification
Lean integration
Python mathematical implementation
license verification
server
internal APIs
```

 Il frontend pubblico non deve duplicare queste strutture.

---

 # 4\. RENDER PRIVATE CORE

 URL:

```
https://aos-private-core.onrender.com
```

 Il deployment è attualmente funzionante.

 Python:

```
3.14.3
```

 Build command:

```
pip install --upgrade pip && pip install -r src/wyp/requirements.txt
```

 Start command:

```
PYTHONPATH=src python -m wyp.server
```

 Il server non utilizza FastAPI.

 IMPORTANTE:

 NON reintrodurre FastAPI automaticamente.

 In precedenza FastAPI era stata introdotta e il deploy falliva per dipendenza mancante.

 La configurazione funzionante attuale non richiede FastAPI.

 Il requirements attuale contiene almeno le dipendenze necessarie alla configurazione crittografica corrente:

```
cryptography
cffi
pycparser
```

 Il server attualmente parte correttamente.

---

 # 5\. SERVER HTTP

 Il private core espone HTTP.

 Endpoint pubblico di stato attraverso il Worker:

```
GET /
```

 Il private core risponde correttamente al root endpoint.

 Il solver utilizza:

```
POST /solve
```

 Il contratto attuale del solver deve essere considerato la fonte reale di verità del backend.

 NON assumere che il vecchio contratto FDM sia ancora il contratto pubblico.

 Il frontend pubblico invia un problema WYP, non i parametri interni del modello FDM.

 Esempio:

```
{
  "problem": "2 + 3"
}
```

 oppure il formato effettivamente stabilito dal private core.

 Il frontend non deve inventare:

```
modulus
dimension
quotient
base
```

 a meno che tali campi siano esplicitamente parte del nuovo contratto pubblico.

---

 # 6\. CLOUDFLARE WORKER

 Worker:

```
https://wyp.auf2026.workers.dev/
```

 Endpoint solver:

```
https://wyp.auf2026.workers.dev/solve
```

 Il Worker è un **gateway HTTP**.

 Architettura:

```
Browser
    |
    v
Cloudflare Worker
    |
    v
https://aos-private-core.onrender.com/solve
```

 Il Worker NON contiene:

```
private key
license key
license token
verification secrets
solver implementation
mathematical implementation
Lean code
FDM implementation
protected logic
```

 Il Worker deve occuparsi solamente di:

```
HTTP
CORS
request validation superficiale
timeout
forwarding
response forwarding
```

 Il Worker non deve diventare un secondo solver.

---

 # 7\. WORKER STATUS

 Il Worker espone:

```
GET /
```

 Risposta prevista:

```
{
  "status": "ONLINE",
  "service": "WYP",
  "gateway": "CLOUDFLARE"
}
```

 Questo endpoint rappresenta lo stato del gateway.

 Non deve essere interpretato automaticamente come prova che ogni componente matematico interno sia disponibile.

 Il controllo effettivo del solver avviene tramite:

```
POST /solve
```

---

 # 8\. WORKER /solve

 Il Worker riceve:

```
POST /solve
```

 dal browser.

 Il Worker:

 1. legge il body;
2. verifica che non sia vuoto;
3. verifica che sia JSON valido;
4. verifica che il JSON sia un object;
5. inoltra il payload al private core;
6. applica un timeout;
7. restituisce la risposta del private core.

 Il Worker non modifica il risultato matematico.

 Il flusso è:

```
Browser
   |
   | POST /solve
   v
Cloudflare
   |
   | POST /solve
   v
Render Private Core
   |
   v
WYP
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

 # 9\. CORS

 Il Worker gestisce CORS.

 Sono previsti:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization, Accept
```

 Il preflight:

```
OPTIONS
```

 deve essere gestito dal Worker.

 Il private core non deve essere chiamato direttamente dal browser.

---

 # 10\. TIMEOUT

 Il Worker utilizza un timeout upstream.

 Configurazione attuale:

```
30000 ms
```

 In caso di timeout deve essere restituito uno stato coerente, ad esempio:

```
{
  "status": "PRIVATE_CORE_TIMEOUT",
  "error": "The protected AOS API did not respond within the configured timeout."
}
```

 In caso di impossibilità di raggiungere il private core:

```
{
  "status": "PRIVATE_CORE_UNAVAILABLE",
  "error": "Unable to reach the protected AOS API."
}
```

---

 # 11\. LICENSING

 Il licensing rimane SERVER-SIDE.

 Modulo:

```
wyp/license
```

 La verifica utilizza Ed25519.

 Le credenziali di licenza non devono essere presenti nella repository pubblica.

 Il private core utilizza variabili d'ambiente.

 Configurazione:

```
WYP_LICENSE_KEY
WYP_LICENSE_PUBLIC_KEY
```

 La funzione di verifica è:

```
require_license()
```

 La verifica comprende, secondo l'implementazione privata:

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

 IMPORTANTE:

 NON inserire il token di licenza nel frontend.

 NON inserire il token nel Worker.

 NON inserire il token in Git.

 NON inserire la private signing key nella repository.

 La configurazione effettiva rimane nel private environment.

---

 # 12\. PUBLIC VERIFICATION KEY

 La public verification key è un elemento crittografico distinto dalla private signing key.

 Il browser non deve riceverla semplicemente perché esiste.

 La verifica della licenza è responsabilità del private core.

 Non introdurre la public key nel JavaScript pubblico senza una precisa necessità architetturale.

---

 # 13\. WYP FDM

 Il private core contiene il modello FDM.

 Componenti concettuali:

```
FDMModel
FDMDerivation
FDMComputation
FDMEngine
```

 L'AOSKernel è lo strato numerico.

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
Jotform
HTML
licensing
natural-language UI
frontend
```

 Questa separazione deve essere mantenuta.

---

 # 14\. FDM PUBLIC CONTRACT

 Il frontend pubblico NON deve essere un'interfaccia diretta al costruttore interno FDM.

 Non richiedere all'utente:

```
modulus
dimension
quotient
```

 solo perché tali valori vengono utilizzati internamente.

 Il tester pubblico deve essere orientato al problema.

 Concettualmente:

```
USER PROBLEM
      |
      v
WYP API
      |
      v
problem interpretation
      |
      v
mathematical engine
      |
      v
FDM / theorems / verification
```

 L'implementazione interna deve rimanere privata.

---

 # 15\. THEOREMS

 I teoremi appartengono al private core.

 Modulo previsto:

```
wyp.theorems
```

 Il frontend pubblico può descrivere:

```
research
method
formalization
verification
theorems
FDM
solver
```

 ma non deve contenere:

```
private theorem implementations
private Lean source
internal registry logic
protected mathematical derivations
```

---

 # 16\. PUBLIC PAGE

 Homepage:

```
https://auf2026.github.io/WYP_system/
```

 La homepage è il punto di ingresso pubblico al progetto.

 Architettura:

```
PUBLIC PAGE

    Jotform
       |
       | separato
       |
       v

    WYP TESTER
       |
       v
    Cloudflare
       |
       v
    Private Core
```

 Il form Jotform e il solver WYP sono due sistemi distinti.

---

 # 17\. JOTFORM

 Il form contatti è gestito da:

```
Jotform
```

 Il form deve rimanere indipendente.

 Il JavaScript pubblico NON deve:

```
intercettare arbitrariamente il submit Jotform
modificare form.action
trasformare il submit in una richiesta WYP
inviare dati del contatto al solver
inviare dati personali al private core
```

 Il flusso corretto è:

```
Jotform
    |
    v
Jotform backend

WYP Tester
    |
    v
Cloudflare
    |
    v
Private Core
```

 Sono due flussi separati.

---

 # 18\. PUBLIC WYP TESTER

 Il tester pubblico utilizza esclusivamente:

```
https://wyp.auf2026.workers.dev/solve
```

 NON deve utilizzare:

```
https://aos-private-core.onrender.com/solve
```

 direttamente dal browser.

 Il browser non deve conoscere l'endpoint Render come destinazione solver.

 Il JavaScript pubblico deve contenere solamente il riferimento al Worker.

 Configurazione:

```
const WYP_API =
    "https://wyp.auf2026.workers.dev/solve";
```

---

 # 19\. PUBLIC JAVASCRIPT

 Il JavaScript pubblico deve essere semplice.

 Responsabilità:

```
UI
tester
POST al Worker
visualizzazione risultato
gestione errori
health/status
eventi tastiera
```

 NON deve contenere:

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

 Il frontend deve rimanere un client.

---

 # 20\. PUBLIC JS — RESPONSE HANDLING

 Il frontend deve distinguere almeno:

```
SUCCESS
LICENSE_REQUIRED
ENGINE_ERROR
INVALID_REQUEST
PRIVATE_CORE_UNAVAILABLE
PRIVATE_CORE_TIMEOUT
PRIVATE_CORE_INVALID_RESPONSE
UNKNOWN STATUS
```

 Il frontend non deve reinterpretare matematicamente il risultato.

 Deve visualizzare il risultato ricevuto dal backend.

 Il JSON del private core è autorevole rispetto al risultato del solver.

---

 # 21\. PUBLIC JS — HEALTH

 Il frontend può controllare:

```
https://wyp.auf2026.workers.dev/
```

 Il controllo attuale utilizza il root endpoint del Worker.

 Non assumere automaticamente che esista:

```
https://wyp.auf2026.workers.dev/health
```

 se il Worker non lo implementa.

 Il browser non deve interrogare direttamente:

```
https://aos-private-core.onrender.com
```

 per il normale status della pagina pubblica.

---

 # 22\. PUBLIC API

 Il frontend espone eventualmente:

```
window.WYP
```

 con funzioni orientate al client, ad esempio:

```
WYP.api
WYP.health
WYP.solve
```

 e può esporre:

```
window.solveWYP(...)
```

 come helper pubblico.

 Questi helper devono rimanere semplici wrapper HTTP.

 NON devono contenere logica matematica.

---

 # 23\. MENU E PAGINE PUBBLICHE

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

 NON introdurre framework inutili.

 NON trasformare il progetto in una SPA se non necessario.

---

 # 24\. CONTENUTO PUBBLICO

 Il contenuto pubblico può descrivere:

```
WYP
AUF2026
ricerca
metodo
approccio matematico
formalizzazione
verifica
FDM
theorems
Lean
solver
licensing
documentazione
```

 Le dichiarazioni pubbliche devono essere formulate in modo tecnico e verificabile.

 Evitare claim assoluti non supportati da risultati pubblicamente verificabili.

 Quando viene dichiarato un risultato scientifico, distinguere chiaramente:

```
implemented
tested
verified
formally verified
published
experimental
research claim
```

 Non presentare come risultato formalmente dimostrato qualcosa che il private core non abbia effettivamente verificato.

---

 # 25\. COSA È STATO RISOLTO

 Sono attualmente risolti:

```
Render deployment
Python 3.14.3
cryptography installation
private core startup
HTTP server
GET /
Cloudflare Worker deployment
Worker status endpoint
Worker /solve gateway
CORS
upstream timeout
public/private separation
Jotform separation
public tester architecture
license configuration
Ed25519 verification infrastructure
```

 Il Render deployment attualmente mostra:

```
[WYP] service=WYP
[WYP] component=FDM
[WYP] version=1.0.0
[WYP] HTTP backend ready
```

 Il Worker è raggiungibile.

---

 # 26\. ERRORI PRECEDENTI DA NON REINTRODURRE

 In precedenza il private core aveva una serie di incompatibilità tra `core/__init__.py` e `core/interpreter.py`.

 Sono comparsi errori del tipo:

```
ImportError:
cannot import name 'StructuredProblemInterpreter'
```

 poi:

```
ImportError:
cannot import name 'CallableInterpreter'
```

 poi:

```
ImportError:
cannot import name 'interpret_mapping'
```

 Questi errori sono stati corretti riallineando gli export/import del core.

 IMPORTANTE:

 Prima di aggiungere un nuovo import in `__init__.py`, verificare che il simbolo esista realmente nel modulo destinazione.

 NON creare alias o classi inesistenti solamente per soddisfare un import.

 NON modificare contemporaneamente molti moduli senza testare l'import chain.

---

 # 27\. REGOLA IMPORTANTE SULL'ARCHITETTURA

 Il progetto ha tre livelli distinti:

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

 Questa separazione deve essere mantenuta.

 NON:

```
Browser → Render
```

 Sì:

```
Browser → Cloudflare → Render
```

 NON:

```
Browser → private solver
```

 Sì:

```
Browser → public API gateway → private solver
```

---

 # 28\. CLOUDFLARE NON È IL SOLVER

 Il Worker non deve diventare il luogo della matematica.

 Non spostare nel Worker:

```
FDM
theorems
AOSKernel
verification
Lean
license verification
```

 Il Worker è solamente:

```
HTTP gateway
```

 L'eventuale utilizzo futuro di Cloudflare AI, Workers AI, Llama o modelli analoghi non modifica automaticamente questa architettura.

 Se in futuro verrà introdotto un LLM, dovrà essere deciso esplicitamente quale ruolo ricopre.

 Una possibile architettura è:

```
User
 |
 v
Public UI
 |
 v
Cloudflare
 |
 v
Private Core
 |
 +--> LLM interpretation
 |
 +--> deterministic solver
 |
 +--> verification
 |
 v
Result
```

 Il modello linguistico non deve diventare automaticamente l'autorità matematica.

---

 # 29\. LLM BOUNDARY

 Il private core può utilizzare un LLM come componente di:

```
interpretazione
classificazione
problem structuring
response composition
```

 ma la matematica deterministica rimane nel solver.

 Concettualmente:

```
USER TEXT
    |
    v
LLM INTERPRETATION
    |
    v
STRUCTURED WYP PROBLEM
    |
    v
DETERMINISTIC SOLVER
    |
    v
VERIFIED RESULT
    |
    v
LLM RESPONSE COMPOSITION
    |
    v
USER
```

 Il modello linguistico NON deve essere considerato il motore matematico autorevole.

---

## 30\. Test end-to-end

 Partiamo dal test più semplice: verificare che il **Worker pubblico** raggiunga effettivamente il **core Render**.

 Da terminale:

```
curl -i https://wyp.auf2026.workers.dev/
```

 Devi ottenere una risposta JSON del Worker simile a:

```
{
  "status": "ONLINE",
  "service": "WYP",
  "gateway": "CLOUDFLARE"
}
```

 Poi:

```
curl -i -X POST \
  https://wyp.auf2026.workers.dev/solve \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"problem":"2 + 2"}'
```

 Qui **non dobbiamo inventare quale sarà il risultato matematico restituito**: deve essere quello prodotto dal tuo core.

 ## 31\. Test diretto del Private Core

 Prima di coinvolgere la pagina pubblica, verifichiamo anche Render:

```
curl -i https://aos-private-core.onrender.com/
```

 Dal log che hai mostrato, questo endpoint è già stato raggiunto correttamente da Render stesso con `200`.

 Poi:

```
curl -i -X POST \
  https://aos-private-core.onrender.com/solve \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"problem":"2 + 2"}'
```

 ## 32\. Se entrambi funzionano

 A quel punto la pagina pubblica può continuare a usare esclusivamente:

```
const WYP_API =
    "https://wyp.auf2026.workers.dev/solve";

const WYP_HEALTH =
    "https://wyp.auf2026.workers.dev/";
```

 **Non**:

```
https://aos-private-core.onrender.com/solve
```

 Il browser deve conoscere soltanto il Worker.

 ## 33\. JotForm

 Il form JotForm rimane separato.

 Il codice del terminale WYP non deve:

```
form.submit();
```

 non deve modificare:

```
form.action
```

 e non deve intercettare il submit del form JotForm.

 La pagina avrà quindi due flussi indipendenti:

```
JotForm
   |
   +----> JotForm

WYP Terminal
   |
   +----> Cloudflare Worker
              |
              +----> Render Private Core
```

 ## 34\. Test dal browser

 Apri la pagina pubblica, inserisci:

```
2 + 2
```

 e premi il pulsante WYP.

 Nel browser, **Network → Fetch/XHR**, deve comparire una richiesta:

```
POST
https://wyp.auf2026.workers.dev/solve
```

 Non deve comparire una richiesta browser verso:

```
aos-private-core.onrender.com
```

 ## 35\. Stato attuale

 Da quello che hai mostrato, il deployment Render è già arrivato a:

```
[WYP] service=WYP
[WYP] component=FDM
[WYP] version=1.0.0
[WYP] HTTP backend ready
==> Your service is live 🎉
```

 Quindi **non tocchiamo Python/core adesso**.

 Il prossimo passaggio concreto è eseguire i due `curl` del punto **30 e 31**. Se mi incolli l'output, procediamo direttamente dal primo eventuale errore, senza modificare componenti che stanno già funzionando.
