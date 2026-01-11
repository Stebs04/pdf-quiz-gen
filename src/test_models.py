import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carichiamo la chiave
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Errore: Chiave API non trovata nel file .env")
else:
    genai.configure(api_key=api_key)

    print("Ecco i modelli disponibili per te:")
    # Chiediamo a Google la lista dei modelli
    try:
        for m in genai.list_models():
            # Filtriamo solo quelli che possono generare testo (generateContent)
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Errore di connessione: {e}")