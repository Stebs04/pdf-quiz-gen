# 🎓 Pdf Quiz Generator

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-App-red) ![Gemini](https://img.shields.io/badge/AI-Gemini%20Flash-orange)

Trasforma i tuoi appunti, slide o libri (PDF e Immagini) in **simulazioni d'esame interattive** con un click.
Basato sul modello **Gemini 1.5 Flash** di Google, questo software non si limita a leggere il testo, ma "vede" grafici, tabelle e formule grazie alla visione multimodale.

---

## ✨ Caratteristiche Nuove

* **🎨 Interfaccia Moderna:** Nuova grafica scura con pulsanti sfumati, barre di progresso colorate e animazioni.
* **🧠 Visione AI:** Carica scansioni o foto di libri; l'IA le legge come un umano.
* **🎭 Imitazione Stile:** Carica vecchi esami e l'IA copierà lo stile e la difficoltà delle domande.
* **🚀 Setup Zero-Config:** Un unico file `start.bat` installa tutto e configura l'ambiente automaticamente.
* **📱 Mobile Friendly:** Funziona perfettamente anche se aperto dal browser del telefono (sulla rete locale).

---

## 🛠️ Installazione e Uso (Guida Rapida)

Non serve saper programmare. Segui questi 3 passi:

### 1. Scarica
* Clicca su **<> Code** in alto a destra > **Download ZIP**.
* Estrai la cartella sul tuo PC.

### 2. Ottieni la Chiave (Gratis)
* Il software usa l'IA di Google. Ti serve una "chiave" per attivarlo.
* Vai su [Google AI Studio](https://aistudio.google.com/app/apikey) e clicca su **Create API Key**.
* Copia la chiave (inizia con `AIza...`).

### 3. Avvia
* Fai doppio click sul file **`start.bat`**.
* La prima volta ti chiederà di incollare la chiave.
* Fatto! Si aprirà automaticamente il tuo browser con l'app pronta.

---

## ❓ Risoluzione Problemi Comuni

**Windows mi blocca l'avvio (Schermata Blu)**
È normale protezione di Windows per i file `.bat` scaricati.
* Clicca su **Ulteriori informazioni**.
* Clicca su **Esegui comunque**.

**L'IA non legge il mio PDF**
Assicurati che il file non sia protetto da password. Se è una scansione molto sfocata, prova a caricarla come immagine (JPG/PNG).

---

## 📂 Struttura del Progetto
* `src/app.py`: Il cuore dell'applicazione (Interfaccia e Logica).
* `src/utils.py`: Gestione caricamento file e sicurezza thread.
* `prompts/`: Istruzioni pedagogiche che guidano l'IA.
* `start.bat`: Script di installazione e avvio automatico.