@echo off
title Installatore Automatico Quiz Gen
cls
echo ========================================================
echo   CONFIGURAZIONE AUTOMATICA GENERATORE QUIZ (1 Click)
echo ========================================================
echo.

REM 1. CONTROLLO PYTHON
echo [1/4] Controllo se Python e' installato...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERRORE] Python non trovato!
    echo Devi installare Python 3.12+ dal sito ufficiale: https://www.python.org/downloads/
    echo IMPORTANTE: Spunta la casella "Add Python to PATH" durante l'installazione.
    pause
    exit
)
echo Python trovato. Procedo.
echo.

REM 2. CREAZIONE AMBIENTE VIRTUALE (Se non esiste)
if not exist "venv" (
    echo [2/4] Creazione della cartella segreta 'venv' (Solo la prima volta)...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Errore nella creazione del venv.
        pause
        exit
    )
) else (
    echo [2/4] Ambiente virtuale gia' esistente. Salto creazione.
)

REM 3. INSTALLAZIONE LIBRERIE
echo.
echo [3/4] Attivazione ambiente e installazione dipendenze...
call venv\Scripts\activate

REM Qui controlliamo se Streamlit è già installato per non perdere tempo ogni volta
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo Installazione librerie in corso (potrebbe volerci un minuto)...
    pip install -r requirements.txt
) else (
    echo Librerie gia' installate.
)

REM 4. AVVIO
echo.
echo [4/4] ==========================================
echo       TUTTO PRONTO! AVVIO DELL'APP IN CORSO...
echo       ==========================================
echo.
streamlit run src\app.py

pause