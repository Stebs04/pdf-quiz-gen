# 🧠 FASE 2: CONFIGURAZIONE AGNO, ENGINE OLLAMA & STYLE PROFILER (100% EMULATION)

> **Riferimento Plan**: [plan.md #fase-2](file:///C:/Users/DeaDS/Documents/Programming%20projects/pdf-quiz-gen/plan.md#5-roadmap-operativa-del-refactoring-6-fasi)
> **Obiettivo**: Creare l'integrazione di connettività verso **Ollama** per inferenza locale, il parser multimodale di PDF/Immagini e il **Modulo 0 (`StyleProfilerAgent`)** responsabile dell'estrazione del "DNA dell'esame".

---

## 🛠️ Checklist delle Attività Operative

- [ ] **Task 2.1: Sviluppo Client Connettore per Ollama (`backend/app/llm/ollama_client.py`)**
  - [ ] Implementare la classe `OllamaEngineManager` che verifica tramite API di Ollama (`http://127.0.0.1:11434/api/tags`) la presenza in locale dei modelli configurati in `.env` (es. `llama3.3` o `qwen2.5` e `llama3.2-vision`).
  - [ ] Implementare un metodo per sollevare un avviso chiaro se il modello non è stato scaricato dall'utente e fornire la riga di comando per eseguirne il pull (`ollama pull llama3.3`).
  - [ ] Predisporre un factory method `get_agno_ollama_model(model_name: str)` che restituisca l'istanza `agno.models.ollama.Ollama(id=model_name)` configurata e pronta per gli Agenti Agno.

- [ ] **Task 2.2: Sviluppo Engine di Ingestione Multimodale (`backend/app/utils/ingestion.py`)**
  - [ ] **Estrazione Testo PDF**: Implementare la funzione `extract_text_from_pdf(file_path: str) -> str` tramite `pypdf` e `pdfplumber` (gestendo layout a colonne e formattazione di tabelle universitarie).
  - [ ] **OCR & Multimodal Vision su Immagini (PNG/JPG)**:
    - [ ] Per appunti scritti a mano, slide o formule fotografate, implementare `extract_content_from_image(file_path: str, vision_model: str) -> str` invocando `Ollama(id="llama3.2-vision")` per trascrivere e descrivere formalmente il contenuto scientifico.
  - [ ] Creare il gestore di sessione file (`backend/app/utils/session_manager.py`) per associare i file di studio e gli esempi del docente a un unico `session_id` UUID su disco (`backend/storage/temp/{session_id}/`).

- [ ] **Task 2.3: Sviluppo Modulo di Estrazione del DNA (`StyleProfilerAgent`)**
  - [ ] Creare `backend/app/agentic/style_profiler.py` che definisce l'Agente Agno per l'analisi e replica dello stile:
    ```python
    from agno.agent import Agent
    from agno.models.ollama import Ollama
    from app.schemas.exam_schemas import StyleDNAProfile

    def build_style_profiler_agent(model_id: str = "llama3.3") -> Agent:
        return Agent(
            name="StyleProfilerAgent",
            model=Ollama(id=model_id),
            response_model=StyleDNAProfile,
            description="Analizzatore esperto del tono, della difficoltà e del design di esami universitari per garantire un'emulazione del 100%.",
            instructions=[
                "Analizza scrupolosamente i documenti di esempio forniti del docente.",
                "Estrai: 1. Il registro linguistico e il lessico scientifico specifico;",
                "2. La strategia di inganno nei distrattori (opzioni di risposta errate);",
                "3. La brevità o lunghezza tipica dei testi dei quesiti;",
                "4. La necessità di citare formule, capitoli o definizioni esatte nelle spiegazioni."
            ]
        )
    ```
  - [ ] Implementare la funzione `profile_exam_style(session_id: str) -> StyleDNAProfile` che aggrega il testo dei documenti del docente e restituisce l'oggetto JSON fortemente tipizzato `StyleDNAProfile`.

---

## ✅ Criteri di Convalida (Acceptance Criteria)

- [ ] Eseguendo uno unit test sul modulo `ollama_client.py`, l'applicazione rileva correttamente se `llama3.3` è in esecuzione in locale.
- [ ] Il modulo `ingestion.py` estrae testo leggibile sia da file `.pdf` testuali sia da immagini `.png` (tramite modello di visione Ollama).
- [ ] `StyleProfilerAgent` invocato su un file di esame universitario restituisce un oggetto Pydantic `StyleDNAProfile` valido senza errori di parsing.
