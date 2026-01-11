@echo off
setlocal
title Installazione e Avvio Quiz AI Generator
cls

echo ========================================================
echo      GENERATORE QUIZ AI - SETUP AUTOMATICO
echo ========================================================
echo.

REM --- 1. CONTROLLO PYTHON ---
echo [1/5] Verifica installazione Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERRORE] Python non trovato!
    echo.
    echo Per favore installa Python dal sito ufficiale: https://www.python.org/downloads/
    echo IMPORTANTE: Durante l'installazione, metti la spunta su "Add Python to PATH".
    echo.
    pause
    exit
)
echo    -> Python trovato.

REM --- 2. CREAZIONE AMBIENTE VIRTUALE ---
if not exist "venv" (
    echo.
    echo [2/5] Creazione ambiente virtuale (prima volta, attendere)...
    python -m venv venv
) else (
    echo [2/5] Ambiente virtuale gia' pronto.
)

REM --- 3. ATTIVAZIONE E INSTALLAZIONE DIPENDENZE ---
echo [3/5] Verifica librerie...
call venv\Scripts\activate

REM Controllo veloce se streamlit esiste, altrimenti installa tutto
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo    -> Installazione dipendenze in corso... (Potrebbe volerci un minuto)
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERRORE] Qualcosa e' andato storto nell'installazione delle librerie.
        pause
        exit
    )
) else (
    echo    -> Librerie gia' installate.
)

REM --- 4. CONFIGURAZIONE CHIAVE API (INTERATTIVA) ---
echo [4/5] Controllo Chiave di Sicurezza...
if not exist ".env" (
    echo.
    echo ========================================================
    echo  ATTENZIONE: Manca la Chiave API di Google (Serve per l'IA)
    echo ========================================================
    echo.
    echo  1. Vai su: https://aistudio.google.com/app/apikey
    echo  2. Crea una chiave e copiala.
    echo.
    set /p APIKEY="Incolla qui la tua chiave (tasto destro per incollare) e premi INVIO: "
    
    REM Scriviamo la chiave nel file .env
    echo GOOGLE_API_KEY=!APIKEY!> .env
    
    echo.
    echo    -> Chiave salvata con successo!
) else (
    echo    -> File .env trovato. Procedo.
)

REM --- 5. AVVIO APP ---
echo.
echo [5/5] Avvio del programma...
echo.
echo ========================================================
echo    PREMI CTRL+C NELLA FINESTRA NERA PER CHIUDERE
echo ========================================================
echo.

streamlit run src/app.py

pause