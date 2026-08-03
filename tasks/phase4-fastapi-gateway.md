# 🔌 FASE 4: API GATEWAY FASTAPI & STREAMING REATTIVO (SSE)

> **Riferimento Plan**: [plan.md #fase-4](file:///C:/Users/DeaDS/Documents/Programming%20projects/pdf-quiz-gen/plan.md#5-roadmap-operativa-del-refactoring-6-fasi)
> **Obiettivo**: Esporre le funzionalità multimodali e agentiche del backend attraverso endpoint REST sicuri e canali Server-Sent Events (SSE) per aggiornare in tempo reale la UI React.

---

## 🛠️ Checklist delle Attività Operative

- [ ] **Task 4.1: Router Upload Materiali & Style Profiling (`backend/app/api/v1/endpoints/materials.py`)**
  - [ ] Implementare l'endpoint `POST /api/v1/materials/upload`:
    - [ ] Accetta un file principale `study_material` (PDF/IMG) e una lista opzionale `example_materials` (PDF/IMG) via `UploadFile`.
    - [ ] Genera un `session_id` (UUID), salva i file temporaneamente e avvia in background l'ingestione e il profiling del DNA (`StyleProfilerAgent`).
    - [ ] Restituisce il `session_id` e l'oggetto `StyleDNAProfile` affinché la UI mostri all'utente i tratti salienti identificati dall'IA.

- [ ] **Task 4.2: Router Generazione Esame (`backend/app/api/v1/endpoints/exams.py`)**
  - [ ] Implementare `POST /api/v1/exams/generate`:
    - [ ] Accetta un JSON con le specifiche dell'esame (`session_id`, `num_closed_questions`, `num_open_questions`, `multiple_choice_ratio`, `emulation_mode: bool`).
    - [ ] Crea un `task_id` di esecuzione asincrona e invoca in background `ExamOrchestratorAgent.generate_complete_exam()`.
    - [ ] Ritorna immediatamente al client il `task_id` per avviare l'ascolto dello stream SSE.

- [ ] **Task 4.3: Router SSE Streaming Progress (`backend/app/api/v1/endpoints/streaming.py`)**
  - [ ] Implementare `GET /api/v1/exams/stream/{task_id}` usando `sse_starlette.EventSourceResponse`:
    - [ ] Streamma gli eventi di log intermedi: `"step": "Analisi capitoli e formule in corso..."`, `"step": "Generazione 15 crocette in stile prof..."`, `"step": "Elaborazione risposte ideali per 3 domande aperte..."`.
    - [ ] Invia l'evento finale `event="complete", data=CompleteExamSimulation_JSON` quando gli Agenti concludono.
    - [ ] Gestisce gracefully gli eventi `event="error"` con messaggio descrittivo.

- [ ] **Task 4.4: Router Correzione Domande Aperte (`POST /api/v1/exams/grade-open`)**
  - [ ] Implementare l'endpoint `POST /api/v1/exams/grade-open` che accetta:
    ```json
    {
      "student_answer": "La memoria virtuale usa pagine e swap...",
      "ideal_answer": "La memoria virtuale è uno schema...",
      "grading_rubric": [ ... ]
    }
    ```
  - [ ] Invoca l'Agente Valutatore (`open_grader.py`) e restituisce in meno di 2 secondi l'oggetto JSON `StudentAnswerEvaluation` (punteggio assegnato e feedback sul compito).

---

## ✅ Criteri di Convalida (Acceptance Criteria)

- [ ] Inviando una richiesta `POST /api/v1/materials/upload` con Postman o cURL con un file di esempio, l'API restituisce un HTTP 200 con `session_id` e il profilo JSON `StyleDNAProfile`.
- [ ] Connettendosi al canale SSE `/api/v1/exams/stream/{task_id}`, il client riceve eventi parziali in tempo reale e il payload completo al termine dell'orchestrazione.
- [ ] L'endpoint `/api/v1/exams/grade-open` valuta correttamente risposte aperte in italiano fornendo feedback puntuali.
