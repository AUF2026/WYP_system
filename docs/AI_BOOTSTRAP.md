# AI BOOTSTRAP — WYP / AUF2026

 ## 0\. SCOPO DI QUESTO FILE

 Questo file è il punto di ripresa del progetto per una nuova istanza AI.

 Se una nuova istanza viene avviata, deve leggere questo file prima di modificare codice.

 NON ripartire da zero.

 NON cambiare architettura senza prima verificare lo stato descritto qui.

 Il progetto in costruzione è **WYP**, parte dell'ecosistema **AUF2026 / AOS-PRIVATE-CORE**.

 Obiettivo generale:

 > costruire un sistema WYP pubblico, consultabile e utilizzabile tramite una pagina GitHub Pages, mantenendo tutta la matematica, i teoremi, il solver e la verifica delle licenze nella repository privata.

---

 # 1\. ARCHITETTURA DEFINITIVA

 L'architettura prevista è:

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
                         ┌────────────┼────────────┐
                         │            │            │
                         ▼            ▼            ▼
                       FDM         THEOREMS      LICENSE
                         │            │            │
                         └────────────┴────────────┘
                                      │
                                      ▼
                           Python / Lean mathematics
                                      │
                                      ▼
                                  WYP SOLVER
                                      │
                                      ▼
                                  JSON result
```

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
- chiavi di verifica che non siano necessarie al browser;
- copie della logica interna del solver.

 Il JavaScript pubblico deve essere solamente un client HTTP.

---

 # 3\. REPOSITORY PRIVATA

 Repository privata:

```
https://github.com/AUF2026/AOS-PRIVATE-CORE
```

 Questa è la repository che contiene il vero motore WYP.

 Il codice privato contiene, tra gli altri:

```
src/wyp/
    fdm/
    theorems/
    license/
    server.py
    ...
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

 Il deploy attualmente FUNZIONA.

 Ultimo stato verificato:

```
==> Build successful 🎉
==> Deploying...
[WYP] service=WYP
[WYP] component=FDM
[WYP] listening=http://0.0.0.0:10000
[WYP] HTTP backend ready
[WYP] 127.0.0.1 - "HEAD / HTTP/1.1" 200 -
==> Your service is live 🎉
```

 Il build command attualmente funzionante è:

```
pip install --upgrade pip && pip install -r src/wyp/requirements.txt
```

 Il start command attualmente funzionante è:

```
PYTHONPATH=src python -m wyp.server
```

 La dipendenza `fastapi` è stata rimossa dal requirements attuale.

 Il requirements attuale installa almeno:

```
cryptography
cffi
pycparser
```

 IMPORTANTE:

 in precedenza era stata introdotta FastAPI e il deploy falliva con:

```
ModuleNotFoundError: No module named 'fastapi'
```

 Questo problema è stato corretto.

 Il server ora parte correttamente senza dipendere da FastAPI.

 NON reintrodurre FastAPI automaticamente.

---

 # 5\. PRIVATE CORE HTTP

 Il private core risponde almeno a:

```
GET /
```

 e attualmente restituisce uno stato del servizio.

 Il deploy ha mostrato:

```
HEAD / HTTP/1.1" 200
GET / HTTP/1.1" 200
```

 È presente anche:

```
/health
```

 Il solver utilizza:

```
POST /solve
```

 MA ATTENZIONE:

 il contratto definitivo di `/solve` è ancora in fase di riallineamento.

 Il vecchio frontend inviava:

```
{
  "problem": "2 + 3"
}
```

 mentre il vecchio server FDM richiedeva direttamente:

```
{
  "modulus": 12,
  "dimension": 3,
  "name": "faure"
}
```

 Questo ha prodotto:

```
WYP INVALID REQUEST

Missing required field: modulus.
```

 Questo comportamento ha identificato il problema architetturale.

 NON bisogna risolverlo mettendo `modulus` e `dimension` nel frontend pubblico.

 La matematica deve essere risolta dal private core.

 Il nuovo contratto deve diventare un contratto di problema/soluzione, non un'esposizione del modello FDM interno.

---

 # 6\. CLOUDFLARE WORKER

 Worker pubblico:

```
https://wyp.auf2026.workers.dev/
```

 Il Worker attuale è un gateway HTTP.

 Architettura:

```
Browser
   ↓
Cloudflare Worker
   ↓
https://aos-private-core.onrender.com/solve
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

 Il test già eseguito sul Worker ha restituito:

```
{
  "status": "ONLINE",
  "service": "WYP",
  "gateway": "CLOUDFLARE"
}
```

 Quindi il Worker è raggiungibile.

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

 Queste sono state configurate su Render.

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

 La licenza di sviluppo fornita durante il lavoro è:

```
{
  "license_id": "WYP-DEV-C50064212F144270ADE265D9B6C9FAD1",
  "customer": "AUF2026-DEVELOPMENT",
  "product": "WYP",
  "issued_at": "2026-09-17T09:29:30.777169Z",
  "expires_at": "2026-10-17T09:29:30.777169Z",
  "environment": "development",
  "features": [
    "all"
  ]
}
```

 NON copiare il token di licenza nel frontend.

 NON inserire la licenza nel Worker.

 NON inserire la licenza in Git.

 La configurazione effettiva deve rimanere su Render.

---

 # 8\. PUBLIC KEY

 La public verification key è un dato pubblico crittografico e viene utilizzata dal modulo di verifica del private core.

 Il browser NON ne ha bisogno.

 NON inserire la public key nel JavaScript pubblico senza una ragione architetturale precisa.

 La verifica della licenza deve avvenire nel private core.

---

 # 9\. SERVER.PY

 Il server è stato modificato per non dipendere da FastAPI.

 La struttura prevista è:

```
HTTP request
    ↓
request validation
    ↓
license verification
    ↓
WYP solver
    ↓
FDM / theorems / Lean / Python
    ↓
JSON response
```

 Il server non deve diventare il luogo dove duplicare la matematica.

 La matematica canonica rimane nei moduli:

```
wyp.fdm
wyp.theorems
```

 e nei relativi sorgenti matematici.

---

 # 10\. WYP FDM

 Esiste un modello FDM canonico.

 Nel codice precedente era rappresentato da:

```
FDMModel
FDMDerivation
FDMComputation
```

 e dalla relazione matematica:

```
M_d(U) = Q(U)^d
```

 IMPORTANTE:

 questa relazione non deve essere trasformata nel contratto pubblico del tester.

 Il frontend pubblico NON deve chiedere:

```
modulus
dimension
quotient
```

 come se l'utente dovesse conoscere l'implementazione interna.

 Il solver deve ricevere un problema e lasciare che il private core determini quali strutture matematiche, teoremi e trasformazioni applicare.

---

 # 11\. THEOREMS

 La repository privata contiene:

```
wyp.theorems
```

 e deve utilizzare i file matematici/Lean previsti dal progetto.

 I teoremi sono parte del motore privato.

 La pagina pubblica può descrivere concettualmente:

 - ricerca;
- metodo;
- formalizzazione;
- verifica;
- teoremi;
- FDM;
- solver;

 ma non deve contenere le implementazioni private.

---

 # 12\. PAGINA PUBBLICA INDEX

 La pagina:

```
https://auf2026.github.io/WYP_system/
```

 è la homepage pubblica.

 Contiene:

 ## Sezione contatti

 Il form è un:

```
Jotform
```

 Non sostituirlo con un POST al WYP core.

 Il form Jotform è un sistema separato dal solver.

 Il JavaScript deve lasciare che il form Jotform funzioni normalmente secondo la sua configurazione.

 NON inviare il form Jotform a:

```
/aos-private-core/solve
```

 NON trasformare il form contatti in una richiesta solver.

---

 # 13\. SOLVER / TESTER PUBBLICO

 Sotto il form Jotform c'è il tester WYP.

 Il tester è una UI pubblica che invia un problema al gateway:

```
https://wyp.auf2026.workers.dev/solve
```

 NON deve chiamare direttamente:

```
https://aos-private-core.onrender.com/solve
```

 Il browser deve passare dal Worker.

 Il tester deve essere concettualmente:

```
USER PROBLEM
    ↓
PUBLIC TESTER
    ↓
CLOUDFLARE
    ↓
PRIVATE WYP
    ↓
THEOREMS / FDM / LEAN / PYTHON
    ↓
RESULT
```

---

 # 14\. NUOVO CONTRATTO DEL TESTER

 Il vecchio JavaScript utilizzava:

```
const WYP_API =
    "https://aos-private-core.onrender.com/solve";
```

 Questo NON è più corretto per la pagina pubblica.

 Deve essere:

```
const WYP_API =
    "https://wyp.auf2026.workers.dev/solve";
```

 Il tester deve inviare un problema generico.

 Esempio concettuale:

```
{
  "problem": "2 + 3"
}
```

 oppure il formato definitivo stabilito dal private core.

 Il frontend non deve inventare parametri FDM.

---

 # 15\. HEALTH CHECK PUBBLICO

 Il frontend può controllare:

```
https://wyp.auf2026.workers.dev/
```

 oppure un endpoint pubblico di status predisposto dal Worker.

 Non è necessario esporre direttamente il Render core al browser.

 Se si usa:

```
/health
```

 deve essere deciso esplicitamente se il Worker deve fare proxy anche di `/health`.

 Non assumere automaticamente che:

```
https://wyp.auf2026.workers.dev/health
```

 esista.

---

 # 16\. JAVASCRIPT PUBBLICO

 Il JavaScript pubblico deve essere semplice.

 Responsabilità:

 - gestione UI;
- gestione tester;
- invio POST al Worker;
- visualizzazione risultato;
- gestione errori;
- eventuale health/status;
- eventuale menu;
- nessuna matematica.

 NON deve contenere:

```
FDM equations
solver logic
theorem implementation
license verification
license token
private key
Render secrets
```

---

 # 17\. MENU / PAGINE PUBBLICHE

 La homepage deve diventare il punto di ingresso al progetto.

 Si prevede un menu semplice, ad esempio:

```
WYP
├── Home
├── About
├── Research
├── Documentation
└── License
```

 Le pagine possono essere:

```
index.html
about.html
research.html
documentation.html
license.html
```

 Eventualmente si può usare un selettore grafico:

```
PAGES ▾
```

 ma senza introdurre framework inutili.

 Il progetto deve rimanere semplice e statico.

---

 # 18\. CONTENUTO PUBBLICO

 La parte pubblica deve essere convincente e informativa.

 Può spiegare:

 - cos'è WYP;
- obiettivi del progetto;
- approccio matematico;
- ruolo della formalizzazione;
- ruolo di Lean;
- concetto di verifica;
- ricerca AUF2026;
- utilizzo del solver;
- licensing;
- documentazione.

 NON deve rivelare l'implementazione privata.

---

 # 19\. COSA È GIÀ STATO RISOLTO

 ## Risolto

 - Render deployment funzionante.
- Python 3.14.3 installato.
- `cryptography` installata.
- Private core avviabile.
- Server in ascolto sulla porta Render.
- `GET /` funzionante.
- Cloudflare Worker raggiungibile.
- Worker restituisce:

```
{
  "status": "ONLINE",
  "service": "WYP",
  "gateway": "CLOUDFLARE"
}
```

 - Variabili di licenza inserite su Render.
- Modulo di verifica Ed25519 presente.
- Private key non presente nella repository.
- Jotform identificato correttamente come form pubblico separato.
- Architettura pubblica/private separata definita.

---

 # 20\. PROBLEMA IDENTIFICATO

 Il precedente tester pubblico chiamava direttamente il Render core:

```
https://aos-private-core.onrender.com/solve
```

 e inviava:

```
{
  "problem": "..."
}
```

 Il server FDM precedente invece richiedeva:

```
modulus
dimension
```

 Risultato:

```
WYP INVALID REQUEST

Missing required field: modulus.
```

 Questo NON deve essere corretto mettendo `modulus` nel frontend.

 Il problema è il contratto API.

 Il solver pubblico deve diventare un'interfaccia al WYP engine, non un'interfaccia al costruttore interno FDM.

---

 # 21\. PROSSIMO LAVORO

 Procedere in quest'ordine.

 ## Step 1 — Private core

 Definire il vero endpoint:

```
POST /solve
```

 con input orientato al problema.

 Il core deve:

```
request
→ license
→ problem parser
→ theorem/FDM engine
→ Lean/Python logic
→ result
```

 ## Step 2 — Test diretto

 Prima testare il Render core senza GitHub Pages.

 Poi testare:

```
Cloudflare Worker
→ Render
```

 ## Step 3 — Public JS

 Modificare il JavaScript della homepage affinché utilizzi:

```
https://wyp.auf2026.workers.dev/solve
```

 e NON Render direttamente.

 ## Step 4 — Jotform

 Lasciare il form Jotform separato.

 Non alterarne il comportamento salvo necessità esplicita.

 ## Step 5 — UI

 Mantenere:

```
Jotform
↓
WYP Solver
```

 nella homepage.

 ## Step 6 — Public pages

 Aggiungere:

```
About
Research
Documentation
License
```

 e un menu di navigazione semplice.

---

 # 22\. REGOLE PER LA NUOVA ISTANZA AI

 Prima di modificare qualcosa:

 1. leggere questo file;
2. controllare la struttura reale della repository;
3. non assumere che il codice precedente sia ancora presente;
4. verificare gli endpoint effettivi;
5. non introdurre FastAPI senza necessità;
6. non mettere matematica privata nella repository pubblica;
7. non mettere licenze/segreti nel frontend;
8. non mettere la private key da nessuna parte nella repository;
9. non far chiamare Render direttamente dal browser;
10. usare Cloudflare Worker come gateway;
11. non confondere Jotform con il solver;
12. non esporre `modulus`, `dimension` o altre strutture interne se non fanno parte del nuovo contratto pubblico;
13. prima modificare il backend, poi il frontend;
14. dopo ogni modifica testare il percorso completo.

---

 # 23\. TEST END-TO-END FINALE

 Il test definitivo deve essere:

```
Browser
  ↓
https://auf2026.github.io/WYP_system/
  ↓
WYP Solver
  ↓
https://wyp.auf2026.workers.dev/solve
  ↓
https://aos-private-core.onrender.com/solve
  ↓
license verification
  ↓
WYP engine
  ↓
FDM / theorems / Lean / Python
  ↓
JSON
  ↓
Cloudflare
  ↓
Browser
```

 Il test non è completo finché non funziona questo percorso.

---

 # 24\. STATO DI RIPRESA

 Punto esatto da cui riprendere:

 > Render è verde e il private core parte correttamente senza FastAPI.\
>  Cloudflare Worker è online.\
>  La licenza è configurata su Render.\
>  Il problema rimasto è riallineare `/solve` affinché sia un vero endpoint WYP solver e non richieda al frontend pubblico i parametri interni FDM.\
>  Dopo questo bisogna rifare il JavaScript della pagina pubblica, mantenendo il form Jotform separato e mettendo sotto di esso il tester WYP che passa esclusivamente dal Cloudflare Worker.

 **NON ripartire dalla configurazione Render.**

 **NON reinstallare FastAPI.**

 **NON spostare la matematica nella repo pubblica.**

 **NON mettere licenze o segreti nel JS.**

 Il prossimo obiettivo concreto è:

```
PRIVATE CORE /solve
        ↓
CLOUDFLARE /solve
        ↓
PUBLIC WYP TESTER
```

 con un singolo flusso funzionante end-to-end.

 Sì: questo `AOSKernel` è coerente come **strato numerico**, ma conferma il problema che stiamo vedendo.

 Il flusso attuale è ancora:

```
pagina pubblica
   ↓
Worker Cloudflare
   ↓
/solve
   ↓
api.solve()
   ↓
build_model()
   ↓
FDMEngine
   ↓
base/modulus + dimension
   ↓
risultato
```

 Quindi una frase tipo:

```
Dimostrami se questa proprietà è vera...
```

 **non può ancora essere risolta**. L'API attuale cerca comunque `modulus`, `dimension`, ecc. Anche se hai messo dei default, non esiste ancora il passaggio:

```
problema libero
   ↓
theorems/registry.py
   ↓
theorem applicabile
   ↓
FDM / AOSKernel
   ↓
verification.py
   ↓
risposta strutturata
```

 ### Quello che abbiamo già correttamente

 Il tuo `AOSKernel` deve rimanere così concettualmente:

```
AOSKernel
   │
   ├── exact
   ├── decimal
   ├── float
   ├── power
   └── identity
```

 Non deve sapere nulla di:

 - HTTP
- licenze
- problemi in linguaggio naturale
- teoremi
- HTML
- Cloudflare
- Jotform

 Questa separazione è giusta.

 ### Il prossimo pezzo da correggere

 Il punto da rifare è **`api.py` \+ `theorems/` \+ `server.py`**, non `AOSKernel`.

 Vogliamo arrivare a qualcosa del genere:

```
{
  "problem": "Dimostra ...",
  "mode": "exact"
}
```

 e il backend deve fare:

```
POST /solve
        │
        ├── require_license()
        │
        ├── riceve "problem"
        │
        ├── analizza il problema
        │
        ├── cerca nel theorem registry
        │
        ├── costruisce il modello matematico
        │
        ├── usa FDMEngine / AOSKernel
        │
        ├── verifica con fdm/verification.py
        │
        └── restituisce una risposta
```

 La **repo privata** rimane il posto dove stanno tutta la matematica e la logica. La GitHub Pages pubblica deve soltanto fare:

```
testo utente
   ↓
Cloudflare Worker
   ↓
PRIVATE CORE
```

 e visualizzare il risultato.

 ### Quindi non fare ancora il test `modulus`

 Quel test sta testando una vecchia API strutturata, non il prodotto che vuoi costruire.

 Per fare il prossimo passaggio correttamente mi servono i contenuti di questi file della repo privata:

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

 In particolare **`theorems/base.py` e `registry.py` sono fondamentali**: è lì che dobbiamo capire come trasformare la richiesta libera del tester in una richiesta matematica realmente risolvibile.

 Poi ti rifaccio l'API in modo che il tester pubblico possa finalmente funzionare così:

```
Problema:
[ Dimostra che ...                              ]

                 [ RISOLVI ]

WYP ENGINE
> PROBLEM RECEIVED
> THEOREM DISCOVERY
> MATHEMATICAL MODEL
> FDM EXECUTION
> INDEPENDENT VERIFICATION
> RESULT

[risposta matematica]
```

 senza mettere **nessuna matematica della repo privata** nella pagina GitHub.io.
