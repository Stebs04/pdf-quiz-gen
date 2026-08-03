# 📦 FASE 1: SCAFFOLDING REPOSITORY, BACKEND FASTAPI & FRONTEND REACT VITE

> **Riferimento Plan**: [plan.md #fase-1](file:///C:/Users/DeaDS/Documents/Programming%20projects/pdf-quiz-gen/plan.md#5-roadmap-operativa-del-refactoring-6-fasi)
> **Obiettivo**: Ristrutturare il repository da progetto singolo Python/Streamlit a un'applicazione moderna con directory separate `backend/` e `frontend/`, preservando ed etichettando il codice `legacy/`.

---

## 🛠️ Checklist delle Attività Operative

- [ ] **Task 1.1: Isolamento e Verifica Directory Legacy**
  - [ ] Assicurarsi che tutti i vecchi sorgenti Streamlit (`src/`, `prompts/`, `start.*`, `requirements.txt`) siano documentati e racchiusi nella cartella `legacy/` senza interferire con le nuove directory di produzione.
  - [ ] Verificare che il file di documentazione [agents.md](file:///C:/Users/DeaDS/Documents/Programming%20projects/pdf-quiz-gen/agents.md) sia presente nella root per futura consultazione architetturale.

- [ ] **Task 1.2: Inizializzazione Workspace Backend (FastAPI + Python 3.12)**
  - [ ] Creare la struttura directory per il backend:
    ```bash
    mkdir -p backend/app/api/v1/endpoints
    mkdir -p backend/app/agentic
    mkdir -p backend/app/llm
    mkdir -p backend/app/schemas
    mkdir -p backend/app/utils
    mkdir -p backend/storage/temp
    ```
  - [ ] Creare il file `backend/requirements.txt` specificando le dipendenze per l'ecosistema moderno:
    ```txt
    fastapi==0.115.6
    uvicorn[standard]==0.32.1
    pydantic==2.10.4
    pydantic-settings==2.7.0
    agno==1.0.1
    google-generativeai==0.8.6
    pypdf==6.6.0
    pdfplumber==0.11.4
    pillow==11.0.0
    python-dotenv==1.0.1
    python-multipart==0.0.20
    sse-starlette==2.1.3
    httpx==0.28.1
    ```
  - [ ] Creare il file `.env.example` in `backend/` con le variabili necessarie per Ollama ed eventuale API key Google di fallback:
    ```env
    OLLAMA_BASE_URL="http://127.0.0.1:11434"
    OLLAMA_DEFAULT_TEXT_MODEL="llama3.3"
    OLLAMA_DEFAULT_VISION_MODEL="llama3.2-vision"
    GOOGLE_API_KEY=""
    ENVIRONMENT="development"
    ```

- [ ] **Task 1.3: Creazione Entry Point del Server Backend**
  - [ ] Creare `backend/app/main.py` impostando l'istanza di FastAPI, abilitando CORS per `http://localhost:5173` (Vite dev server) e un endpoint di health check (`GET /health`):
    ```python
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(
        title="University Quiz AI — Next-Gen API Gateway",
        description="API Gateway multimodale e agentico con Agno e Ollama.",
        version="2.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["System"])
    async def health_check():
        return {"status": "ok", "version": "2.0.0", "engine": "agno-ollama"}
    ```

- [ ] **Task 1.4: Scaffolding del Frontend React 19 + TypeScript (Vite)**
  - [ ] Creare la cartella `frontend/` e inizializzare il progetto Vite (senza interazione utente):
    ```bash
    npx -y create-vite@latest frontend --template react-ts
    ```
  - [ ] Aggiornare `frontend/package.json` installando dipendenze di supporto per design system e icone moderne:
    ```bash
    cd frontend && npm install lucide-react framer-motion clsx tailwind-merge
    ```
  - [ ] Configurare in `frontend/vite.config.ts` un proxy locale affinché le chiamate a `/api` siano inoltrate su `http://127.0.0.1:8000`:
    ```typescript
    import { defineConfig } from 'vite'
    import react from '@vitejs/plugin-react'

    export default defineConfig({
      plugins: [react()],
      server: {
        port: 5173,
        proxy: {
          '/api': {
            target: 'http://127.0.0.1:8000',
            changeOrigin: true,
          }
        }
      }
    })
    ```

---

## ✅ Criteri di Convalida (Acceptance Criteria)

- [ ] L'ambiente Python del backend installa tutte le dipendenze (`pip install -r backend/requirements.txt`) senza conflitti.
- [ ] Il server FastAPI si avvia con `uvicorn app.main:app --reload` e risponde `{"status": "ok"}` su `http://127.0.0.1:8000/health`.
- [ ] Il progetto frontend compila regolarmente con `npm run dev` in `frontend/` senza errori TypeScript.
