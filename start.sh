#!/bin/bash

# Titolo e pulizia schermo
clear
echo "=========================================="
echo "       AVVIO QUIZ GENERATOR AI (Mac/Linux)"
echo "=========================================="
echo ""

# --- 1. RICERCA PYTHON ---
echo "[1/4] Controllo installazione Python..."

if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    echo "   - Python 3 trovato."
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
    echo "   - Python trovato."
else
    echo ""
    echo "[ERRORE] Python non trovato."
    echo "Per favore installalo da: https://www.python.org/downloads/"
    exit 1
fi

# --- 2. SETUP AMBIENTE VIRTUALE ---
if [ -d "venv" ]; then
    echo "   - Ambiente virtuale già presente."
else
    echo ""
    echo "[2/4] Creazione ambiente isolato (venv)..."
    $PYTHON_CMD -m venv venv
fi

# --- 3. ATTIVAZIONE E LIBRERIE ---
echo ""
echo "[3/4] Verifica librerie necessarie..."

# Attivazione venv (Percorso specifico per Mac/Linux)
source venv/bin/activate

# Controllo se streamlit è installato
if pip show streamlit > /dev/null 2>&1; then
    echo "   - Librerie già installate."
else
    echo "   - Installazione dipendenze in corso (attendi)..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERRORE] Installazione librerie fallita."
        exit 1
    fi
fi

# --- 4. CHECK API KEY E AVVIO ---
echo ""
echo "[4/4] Avvio applicazione..."

if [ -f ".env" ]; then
    echo "   - Configurazione trovata."
else
    echo ""
    echo "=========================================="
    echo " CONFIGURAZIONE INIZIALE (Solo 1a volta)"
    echo "=========================================="
    echo " Per funzionare, serve una chiave Google (gratis)."
    echo " Prendila qui: https://aistudio.google.com/app/apikey"
    echo ""
    read -p "Incolla la tua chiave API e premi INVIO: " APIKEY
    echo "GOOGLE_API_KEY=$APIKEY" > .env
fi

# --- LANCIO ---
echo ""
echo "   Lancio interfaccia grafica..."
echo "   (Premi CTRL+C per terminare)"
echo ""
streamlit run src/app.py