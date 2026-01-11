import google.generativeai as genai
import time
import os
import uuid 

def carica_file_su_gemini(uploaded_file):
    """
    Funzione robusta per caricare file su Gemini.
    Gestisce:
    1. Salvataggio temporaneo su disco (necessario per le API).
    2. Nomi univoci (UUID) per evitare conflitti su Windows.
    3. Upload e Attesa attiva (polling) finché Google non ha processato il file.
    4. Pulizia automatica del file temporaneo.
    """
    
    # Generiamo un nome univoco per evitare che due file si sovrascrivano
    # es: temp_8f3a2b1c.pdf
    nome_file_temporaneo = f"temp_{uuid.uuid4()}.pdf"
    
    try:
        # 1. Scriviamo il file ricevuto dalla RAM al Disco
        with open(nome_file_temporaneo, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 2. Determiniamo il tipo MIME corretto (PDF o Immagine)
        mime_type = "application/pdf"
        if uploaded_file.type:
            mime_type = uploaded_file.type
            
        # 3. Caricamento su server Google
        print(f"--> Uploading: {nome_file_temporaneo} ({mime_type})")
        file_gemini = genai.upload_file(path=nome_file_temporaneo, mime_type=mime_type)
        
        # 4. Loop di attesa (Google deve "leggere" il file prima di usarlo)
        while file_gemini.state.name == "PROCESSING":
            time.sleep(1) # Aspettiamo 1 secondo
            file_gemini = genai.get_file(file_gemini.name) # Chiediamo lo stato aggiornato

        # 5. Verifica finale
        if file_gemini.state.name == "FAILED":
            raise ValueError("Errore lato Google: impossibile processare il file.")

        print(f"--> Ready: {file_gemini.name}")
        return file_gemini

    finally:
        # 6. Pulizia (Blocco Finally viene eseguito SEMPRE)
        # Cerchiamo di cancellare il file temporaneo per non riempire il disco
        time.sleep(0.5) # Piccolo delay per permettere a Windows di rilasciare il file
        if os.path.exists(nome_file_temporaneo):
            try:
                os.remove(nome_file_temporaneo)
            except Exception:
                # Se non riusciamo a cancellarlo subito (file lock), lo ignoriamo.
                # Non è critico per il funzionamento dell'app.
                print(f"Info: Impossibile cancellare subito {nome_file_temporaneo}")