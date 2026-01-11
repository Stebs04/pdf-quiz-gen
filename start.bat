@echo off
setlocal
title Installazione Quiz AI
cls

echo ==========================================
echo   SETUP GENERATORE QUIZ (Versione Stabile)
echo ==========================================
echo.

REM --- 1. CERCO PYTHON (Metodo Lineare) ---
echo [1/4] Cerco Python...

REM Provo 'python'
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto python_trovato
)

REM Provo 'py' (Launcher di Windows)
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto python_trovato
)

REM Provo 'python3'
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python3
    goto python_trovato
)

REM Se arrivo qui, Python non c'è
echo.
echo [ERRORE] Python non trovato.
echo Installa Python da: https://www.python.org/downloads/
echo IMPORTANTE: Spunta "Add Python to PATH" durante l'installazione.
pause
exit /b

:python_trovato
echo    - Usiamo il comando: %PYTHON_CMD%

REM --- 2. AMBIENTE VIRTUALE ---
if exist "venv" goto venv_pronto
echo.
echo [2/4] Creo ambiente virtuale...
%PYTHON_CMD% -m venv venv
:venv_pronto

REM --- 3. LIBRERIE ---
echo.
echo [3/4] Controllo librerie...
call venv\Scripts\activate

pip show streamlit >nul 2>&1
if %errorlevel% equ 0 goto librerie_ok

echo    - Installazione dipendenze in corso...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERRORE] Installazione fallita.
    pause
    exit /b
)
:librerie_ok

REM --- 4. CHIAVE E AVVIO ---
echo.
echo [4/4] Avvio...

if exist ".env" goto avvia_tutto

echo.
echo ========================================
echo  MANCA LA CHIAVE GOOGLE (Solo prima volta)
echo ========================================
echo  Ottienila qui: https://aistudio.google.com/app/apikey
echo.
set /p APIKEY="Incolla la chiave e premi INVIO: "
echo GOOGLE_API_KEY=%APIKEY%> .env

:avvia_tutto
cls
echo Avvio del Quiz in corso...
streamlit run src/app.py
pause