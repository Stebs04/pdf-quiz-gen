@echo off
setlocal
title QuizGen AI - Launcher
cls

echo ==========================================
echo        AVVIO QUIZ GENERATOR AI
echo ==========================================
echo.

REM --- 1. RICERCA PYTHON (Approccio Lineare) ---
echo [1/4] Controllo installazione Python...

REM Proviamo il comando 'python' standard
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto python_found
)

REM Proviamo il launcher 'py' (comune su Windows)
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto python_found
)

REM Proviamo 'python3' (comune su Linux/Mac o setup specifici)
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python3
    goto python_found
)

REM Nessun Python trovato
echo.
echo [ERRORE] Python non trovato.
echo Per favore installalo da: [https://www.python.org/downloads/](https://www.python.org/downloads/)
echo IMPORTANTE: Spunta "Add Python to PATH" durante l'installazione.
pause
exit /b

:python_found
echo    - Python trovato (comando: %PYTHON_CMD%)

REM --- 2. SETUP AMBIENTE VIRTUALE ---
if exist "venv" goto venv_ready
echo.
echo [2/4] Creazione ambiente isolato (venv)...
%PYTHON_CMD% -m venv venv
:venv_ready

REM --- 3. CONTROLLO LIBRERIE ---
echo.
echo [3/4] Verifica librerie necessarie...
call venv\Scripts\activate

REM Controlliamo se streamlit Ã¨ giÃ  installato
pip show streamlit >nul 2>&1
if %errorlevel% equ 0 goto libs_installed

echo    - Installazione dipendenze in corso (attendi)...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERRORE] Installazione librerie fallita.
    pause
    exit /b
)
:libs_installed

REM --- 4. CHECK API KEY E AVVIO ---
echo.
echo [4/4] Avvio applicazione...

if exist ".env" goto start_app

echo.
echo ==========================================
echo  CONFIGURAZIONE INIZIALE (Solo 1a volta)
echo ==========================================
echo  Per funzionare, serve una chiave Google (gratis).
echo  Prendila qui: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
echo.
set /p APIKEY="Incolla la tua chiave API e premi INVIO: "
echo GOOGLE_API_KEY=%APIKEY%> .env

:start_app
cls
echo.
echo    Lancio interfaccia grafica...
echo    (Si aprira il browser automaticamente)
echo    Per terminare premere CTRL+C
echo.
streamlit run src/app.py
pause