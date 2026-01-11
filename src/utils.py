import google.generativeai as genai
import time
import os
import uuid  # Libreria per creare nomi casuali unici

def carica_file_su_gemini(uploaded_file):
    """
    Gestisce il caricamento su Gemini in modo sicuro per Windows.
    Usa nomi di file univoci e gestisce gli errori di cancellazione.
    """
    
    # 1. CREIAMO UN NOME UNIVOCO
    # Invece di "temp.pdf", generiamo "temp_3a4b5c...pdf"
    # Così se carichi 2 file, avranno nomi diversi e non andranno in conflitto.
    nome_file_temporaneo = f"temp_{uuid.uuid4()}.pdf"
    
    try:
        # 2. SALVATAGGIO SU DISCO
        with open(nome_file_temporaneo, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 3. UPLOAD SU GOOGLE
        # Determiniamo il tipo di file (pdf, jpg, png)
        mime_type = "application/pdf" # Default
        if uploaded_file.type:
            mime_type = uploaded_file.type
            
        print(f"Caricamento file temporaneo: {nome_file_temporaneo}...")
        file_gemini = genai.upload_file(path=nome_file_temporaneo, mime_type=mime_type)
        
        # 4. ATTESA ELABORAZIONE (Polling)
        while file_gemini.state.name == "PROCESSING":
            time.sleep(2)
            file_gemini = genai.get_file(file_gemini.name)

        if file_gemini.state.name == "FAILED":
            raise ValueError("Gemini non è riuscito a elaborare questo file.")

        print(f"File pronto su Gemini: {file_gemini.name}")
        return file_gemini

    finally:
        # 5. PULIZIA SICURA (Anti-Crash)
        # Il blocco 'finally' viene eseguito SEMPRE, anche se c'è un errore prima.
        
        # Aspettiamo 1 secondo per dare tempo a Windows di "rilasciare" il file
        time.sleep(1)
        
        if os.path.exists(nome_file_temporaneo):
            try:
                os.remove(nome_file_temporaneo)
            except Exception as e:
                # Se Windows blocca il file, lo scriviamo solo nel terminale ma NON fermiamo il programma
                print(f"⚠️ Avviso Windows: Impossibile cancellare subito {nome_file_temporaneo}. Verrà eliminato al riavvio.")