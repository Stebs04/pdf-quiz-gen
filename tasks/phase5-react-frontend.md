# 🎨 FASE 5: FRONTEND REACT 19 + TYPESCRIPT & DESIGN SYSTEM WOW

> **Riferimento Plan**: [plan.md #fase-5](file:///C:/Users/DeaDS/Documents/Programming%20projects/pdf-quiz-gen/plan.md#5-roadmap-operativa-del-refactoring-6-fasi)
> **Obiettivo**: Sviluppare un'interfaccia utente web reattiva, moderna e mozzafiato con React 19, TypeScript e Vite, implementando la palette HSL Cyber Academic Dark Mode, animazioni fluide con framer-motion e un'Arena d'Esame ad alte prestazioni.

---

## 🛠️ Checklist delle Attività Operative

- [ ] **Task 5.1: Architettura CSS & Token Design System (`frontend/src/index.css`)**
  - [ ] Impostare le variabili CSS personalizzate con palette HSL ottimizzata per affaticamento visivo ridotto:
    ```css
    :root {
      --bg-main: hsl(220, 26%, 8%);
      --bg-surface: rgba(255, 255, 255, 0.04);
      --bg-surface-hover: rgba(255, 255, 255, 0.08);
      --border-subtle: rgba(255, 255, 255, 0.08);
      --accent-cyan: hsl(190, 90%, 50%);
      --accent-mint: hsl(150, 85%, 55%);
      --accent-coral: hsl(15, 90%, 55%);
      --text-main: hsl(210, 20%, 95%);
      --text-muted: hsl(215, 15%, 65%);
    }
    ```
  - [ ] Implementare classi di utilità per il **Glassmorphism** (`backdrop-blur-md`, bordi con gradiente sottile, ombre neon hover).

- [ ] **Task 5.2: Header & Indicatori di Stato (`frontend/src/components/layout/Navbar.tsx`)**
  - [ ] Costruire la barra superiore con logo, titolo del corso e un badge interattivo che indica lo stato del modello locale Ollama (`🟢 Connected to Ollama (llama3.3)`).

- [ ] **Task 5.3: Sidebar Ingestione & "Exam DNA Viewer" (`frontend/src/components/sidebar/`)**
  - [ ] `MaterialUploader.tsx`: Creare un'area di Drag-and-Drop multimediale che mostri il progresso del caricamento del PDF di studio e dei file di esempio del prof.
  - [ ] `StyleDNACard.tsx`: Dopo l'upload, visualizzare con un'animazione a comparsa i 4 parametri emulativi identificati da `StyleProfilerAgent` (es. badge `"Linguaggio: Formale Medico"`, `"Distrattori: Molto Insidiosi"`).

- [ ] **Task 5.4: Configurazione Esame (`frontend/src/components/configurator/ExamConfigForm.tsx`)**
  - [ ] Costruire i controlli per calibrare la prova:
    - [ ] Slider numero domande chiuse (10 - 50).
    - [ ] Segmented Control o Toggle per il rapporto Singola / Multipla (es. `100% Singola`, `70% Singola / 30% Multipla`).
    - [ ] Slider numero domande aperte (0 - 10).
    - [ ] Switch interattivo con bagliore neon: **"🔥 100% Professor Emulation Mode"**.

- [ ] **Task 5.5: Interactive Quiz Arena (`frontend/src/components/arena/`)**
  - [ ] **`QuizHeader.tsx`**: Contatore temporale, barra di avanzamento graduata e griglia di navigazione rapida tra le domande (da Q1 a QN, con indicatori per corrette/errate/da valutare).
  - [ ] **`SingleChoiceCard.tsx` & `MultiChoiceCard.tsx`**:
    - [ ] Schede per quesiti a crocette con radio button e checkbox customizzate.
    - [ ] Feedback immediato allo schiacciamento di "Conferma" con evidenziazione animata del distrattore e cassetto espandibile della spiegazione del prof.
  - [ ] **`OpenQuestionCard.tsx`**:
    - [ ] Scheda per domande aperte con area editor auto-espandibile per la risposta dello studente.
    - [ ] Bottone **"✨ Valuta la mia risposta con AI"**: al click, chiama `/api/v1/exams/grade-open` e mostra l'effettivo voto (es. `28/30`), la **Risposta Ideale** del prof e la **Rubrica di Correzione** con evidenziati i concetti toccati/mancanti.

- [ ] **Task 5.6: Scoreboard & Analisi del Risultato (`frontend/src/components/results/ScoreDashboard.tsx`)**
  - [ ] Alla fine della simulazione, visualizzare:
    - [ ] Il voto percentuale totale e l'equivalente universitario (es. `30/30 e Lode`, `26/30`, `Non Superato`).
    - [ ] Breakdown della performance per argomento (`topic_tag`).
    - [ ] Bottone animato "🔄 Nuova Simulazione (Stesso Stile)".

---

## ✅ Criteri di Convalida (Acceptance Criteria)

- [ ] L'applicazione React si carica in modo istantaneo e fluido in meno di 1 secondo su `http://localhost:5173`.
- [ ] Il form di configurazione trasmette i parametri corretti al backend e visualizza il caricamento in tempo reale tramite gli eventi SSE.
- [ ] L'interfaccia si adatta perfettamente (responsive design) a schermi desktop e tablet.
- [ ] L'animazione di valutazione della domanda aperta restituisce feedback chiaro senza bloccare l'interfaccia.
