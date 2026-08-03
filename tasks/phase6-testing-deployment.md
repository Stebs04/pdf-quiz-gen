# 🧪 FASE 6: INTEGRATION TESTING, VALIDAZIONE EMULAZIONE 100% & DEPLOYMENT

> **Riferimento Plan**: [plan.md #fase-6](file:///C:/Users/DeaDS/Documents/Programming%20projects/pdf-quiz-gen/plan.md#5-roadmap-operativa-del-refactoring-6-fasi)
> **Obiettivo**: Eseguire i test di verifica di fine-to-end sull'architettura locale Ollama + Agno + FastAPI + React, convalidando la fedeltà del 100% rispetto agli esami reali e unificando gli script di avvio.

---

## 🛠️ Checklist delle Attività Operative

- [ ] **Task 6.1: Suite di Test Automatizzati del Backend (`backend/tests/`)**
  - [ ] Creare uno script `test_e2e_generation.py` utilizzando `pytest` e `httpx.AsyncClient`:
    - [ ] Simula l'upload di una dispensa universitaria in formato PDF.
    - [ ] Simula l'upload di una vecchia prova d'esame e verifica che l'endpoint restituisca lo `StyleDNAProfile` atteso.
    - [ ] Invia una richiesta di generazione di un esame misto (10 crocette singole, 5 crocette multiple, 2 aperte) e verifica che tutti gli schemi Pydantic siano conformi.

- [ ] **Task 6.2: Benchmark e Ottimizzazione Modelli Ollama Locali**
  - [ ] Misurare il tempo di risposta totale di `ClosedQuestionsAgent` e `OpenQuestionsAgent` in esecuzione parallela con `Ollama(id="llama3.3")`.
  - [ ] Implementare una logica di fallback o avviso nella UI in caso l'hardware dell'utente sia privo di GPU dedicata, suggerendo di passare a un modello più leggero (es. `qwen2.5:7b` o `llama3.2:3b`).

- [ ] **Task 6.3: Validazione Qualitativa della 100% Style Emulation**
  - [ ] Condurre una verifica comparativa affiancando una vera prova d'esame del docente e il test generato dal sistema, assicurandosi che:
    - [ ] I termini tecnici ed espressioni formali del docente appaiano nelle domande.
    - [ ] I distrattori (opzioni errate) non siano ovvi, ma rispecchino l'insidia del test reale.
    - [ ] Le spiegazioni e le risposte ideali alle domande aperte contengano la stessa profondità analitica.

- [ ] **Task 6.4: Aggiornamento Launcher Unificati (`start.bat` & `start.sh`)**
  - [ ] Aggiornare `start.bat` per Windows in modo che un singolo doppio clic:
    1. Verifichi e attivi il virtual environment in `backend/venv`.
    2. Avvii in background il server API FastAPI su porta `8000`.
    3. Controlli se `node` / `npm` è installato e avvii in parallelo il dev server Vite (`npm run dev --prefix frontend`) su porta `5173`.
    4. Apra automaticamente il browser all'indirizzo `http://localhost:5173`.
  - [ ] Aggiornare `start.sh` per macOS/Linux con la medesima logica POSIX pulita e gestione del segnale `CTRL+C` (`trap 'kill $(jobs -p)' EXIT`) per arrestare insieme FastAPI e Vite al termine.

---

## ✅ Criteri di Convalida (Acceptance Criteria)

- [ ] L'esecuzione della suite `pytest backend/tests/` passa al 100% in meno di 60 secondi in presenza di Ollama locale.
- [ ] Facendo doppio clic su `start.bat` in Windows (o `./start.sh` in Mac/Linux), si avviano automaticamente sia il backend che il frontend e il browser si apre sull'interfaccia React funzionante.
- [ ] Nessun file o log residuo viene generato all'esterno della cartella temporanea del backend (`backend/storage/temp/`).
