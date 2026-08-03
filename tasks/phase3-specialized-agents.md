# 🎯 FASE 3: SVILUPPO AGENTI SPECIALIZZATI IN AGNO (CROCETTE & APERTE)

> **Riferimento Plan**: [plan.md #fase-3](file:///C:/Users/DeaDS/Documents/Programming%20projects/pdf-quiz-gen/plan.md#5-roadmap-operativa-del-refactoring-6-fasi)
> **Obiettivo**: Implementare in Agno i due Agenti Specializzati responsabili della creazione di domande a risposta chiusa (singola/multipla) e di domande aperte con rubrica analitica di valutazione, coordinati da un Orchestratore.

---

## 🛠️ Checklist delle Attività Operative

- [ ] **Task 3.1: Configurazione Schemi Dati Pydantic (`backend/app/schemas/exam_schemas.py`)**
  - [ ] Implementare i modelli Pydantic v2 precisi come da contratto dati ([plan.md - Sezione 3](file:///C:/Users/DeaDS/Documents/Programming%20projects/pdf-quiz-gen/plan.md#3--contratti-dati--schemi-pydantic-v2)):
    - [ ] `ClosedQuestionItem`: include il campo `question_type` (`single_choice` o `multiple_choice`), `options` (4-5 stringhe) e `correct_indices` (array di interi).
    - [ ] `GradingCriterion`: singolo criterio della rubrica (`concept`, `max_points`, `required_keywords`).
    - [ ] `OpenQuestionItem`: include la traccia discorsiva, `ideal_answer` (la risposta del professore al 100% di fedeltà) e la `grading_rubric`.
    - [ ] `StudentAnswerEvaluation`: schema del risultato di correzione live (`score_awarded`, `max_possible_score`, `feedback_summary`, `missing_concepts`).

- [ ] **Task 3.2: Sviluppo Agente 1 — `ClosedQuestionsAgent` (`backend/app/agentic/closed_agent.py`)**
  - [ ] Creare il factory `build_closed_questions_agent(model_id: str = "llama3.3") -> Agent` in Agno, associando `response_model=List[ClosedQuestionItem]`.
  - [ ] Strutturare il System Prompt dinamico che inietta il `StyleDNAProfile` affinché l'agente:
    - [ ] Copra uniformemente tutto il materiale di studio senza concentrarsi solo sull'inizio.
    - [ ] Alterni domande di pura memoria, domande su differenze tra concetti e problemi di calcolo o ragionamento.
    - [ ] Nel caso di `multiple_choice`, formuli domande dove da 2 a 3 opzioni siano corrette e richiedano la selezione di caselle multiple.
    - [ ] Generi distrattori (opzioni sbagliate) conformi alle regole del prof (`distractor_subtlety`).

- [ ] **Task 3.3: Sviluppo Agente 2 — `OpenQuestionsAgent` (`backend/app/agentic/open_agent.py`)**
  - [ ] Creare il factory `build_open_questions_agent(model_id: str = "llama3.3") -> Agent` per produrre `List[OpenQuestionItem]`.
  - [ ] Strutturare il System Prompt affinché ogni domanda aperta sia corredata da:
    - [ ] **Traccia (question_text)**: problema di teoria o sviluppo con eventuale contesto pratico/case study.
    - [ ] **Risposta Ideale (ideal_answer)**: risposta esplicativa completa, formale e rigorosa come scritta dal docente sul libro/appunti.
    - [ ] **Rubrica Analitica (grading_rubric)**: scomposizione dei 30 punti in 3-5 criteri quantitativi misurabili.

- [ ] **Task 3.4: Sviluppo del Valutatore di Risposte Aperte (`backend/app/agentic/open_grader.py`)**
  - [ ] Creare l'Agente Valutatore `build_open_answer_grader(model_id: str = "llama3.3") -> Agent` che accetta come input `(student_answer, ideal_answer, grading_rubric)`.
  - [ ] Impostare `response_model=StudentAnswerEvaluation` per restituire un voto analitico e la lista esatta dei concetti saltati o errati dall'utente.

- [ ] **Task 3.5: Creazione Orchestratore dell'Esame (`backend/app/agentic/orchestrator.py`)**
  - [ ] Implementare `async def generate_complete_exam(...)` che:
    1. Prende dal frontend il numero richiesto di domande chiuse e aperte e la percentuale di crocette singole/multiple.
    2. Esegue via `asyncio.gather` (in parallelo) la generazione su `ClosedQuestionsAgent` e `OpenQuestionsAgent`.
    3. Assembla e restituisce il payload unificato `CompleteExamSimulation`.

---

## ✅ Criteri di Convalida (Acceptance Criteria)

- [ ] L'esecuzione di test su `ClosedQuestionsAgent` genera un array dove tutte le domande `single_choice` hanno len(`correct_indices`) == 1 e le `multiple_choice` hanno len(`correct_indices`) >= 2.
- [ ] L'esecuzione di `OpenQuestionsAgent` restituisce domande la cui somma di `max_points` nella rubrica è coerente con `max_total_points` (es. 30.0).
- [ ] Il modulo `open_grader.py` punisce opportunamente con un voto più basso una risposta incompleta rispetto a una completa.
