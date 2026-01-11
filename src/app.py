import streamlit as st
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from utils import carica_file_su_gemini

# Carica le variabili d'ambiente (il file .env)
load_dotenv()

st.set_page_config(page_title="Quiz Interattivo AI", page_icon="🎮", layout="centered")

# --- FUNZIONI DI SUPPORTO ---
def leggi_prompt(nome_file):
    """Legge il contenuto di un file di testo dalla cartella prompts."""
    # Risaliamo di un livello da src/ per trovare la cartella prompts/
    percorso_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    percorso_file = os.path.join(percorso_base, "prompts", nome_file)
    
    try:
        with open(percorso_file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Errore: Non trovo il file {nome_file} nella cartella prompts!")
        return ""

def pulisci_json(testo_response):
    """Pulisce la risposta di Gemini per estrarre solo il JSON puro."""
    testo_response = testo_response.replace("```json", "").replace("```", "")
    start = testo_response.find("[")
    end = testo_response.rfind("]") + 1
    if start != -1 and end != -1:
        return testo_response[start:end]
    return testo_response

# --- SESSION STATE (Memoria del Gioco) ---
if "quiz_data" not in st.session_state: st.session_state.quiz_data = None
if "current_index" not in st.session_state: st.session_state.current_index = 0
if "score" not in st.session_state: st.session_state.score = 0
if "answer_submitted" not in st.session_state: st.session_state.answer_submitted = False

# --- CONFIGURAZIONE API ---
api_key = os.getenv("GOOGLE_API_KEY")

st.title("🎮 Quiz Interattivo Universitario")

# Controllo Chiave: Se non c'è nel file .env, mostriamo un avviso gentile
if not api_key:
    st.warning("⚠️ Chiave API non trovata.")
    st.info("Per usare questa app, crea un file chiamato '.env' nella cartella principale e scrivici dentro: GOOGLE_API_KEY=la_tua_chiave")
    st.stop()

genai.configure(api_key=api_key)

# --- SIDEBAR (Input) ---
with st.sidebar:
    st.header("📂 Carica i tuoi documenti")
    uploaded_file_studio = st.file_uploader("1. Documento Studio (PDF/IMG)", type=["pdf", "png", "jpg"], key="studio")
    st.markdown("---")
    
    # MODIFICA: accept_multiple_files=True permette di caricare più esempi
    uploaded_files_esempi = st.file_uploader(
        "2. Esempi di Stile (Caricane quanti ne vuoi)", 
        type=["pdf", "png", "jpg"], 
        key="esempi", 
        accept_multiple_files=True
    )
    st.markdown("---")
    
    if st.button("🚀 Genera Nuovo Quiz", type="primary"):
        # Reset del gioco
        st.session_state.quiz_data = None
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.answer_submitted = False
        st.rerun()

# --- LOGICA APPLICAZIONE ---
if st.session_state.quiz_data is None:
    if uploaded_file_studio:
        with st.spinner("🧠 Sto leggendo i file e analizzando lo stile..."):
            try:
                # 1. LEGGIAMO I PROMPT BASE
                prompt_base_text = leggi_prompt("base.txt")
                prompt_style_text = leggi_prompt("style.txt")

                # 2. COSTRUIAMO LA LISTA MULTIMODALE
                contenuto_richiesta = []
                
                # Aggiungiamo le istruzioni principali
                contenuto_richiesta.append(prompt_base_text)

                # Aggiungiamo il documento di studio
                st.text("Caricamento documento studio su Gemini...")
                file_studio_proc = carica_file_su_gemini(uploaded_file_studio)
                contenuto_richiesta.append("--- INIZIO DOCUMENTO STUDIO ---")
                contenuto_richiesta.append(file_studio_proc)
                contenuto_richiesta.append("--- FINE DOCUMENTO STUDIO ---")

                # Aggiungiamo GLI esempi (Ciclo su tutti i file caricati)
                if uploaded_files_esempi:
                    contenuto_richiesta.append(prompt_style_text)
                    contenuto_richiesta.append("--- INIZIO DOCUMENTI ESEMPIO ---")
                    
                    for i, file_esempio in enumerate(uploaded_files_esempi):
                        st.text(f"Caricamento esempio {i+1}: {file_esempio.name}...")
                        file_proc = carica_file_su_gemini(file_esempio)
                        contenuto_richiesta.append(f"Esempio #{i+1}:")
                        contenuto_richiesta.append(file_proc)
                    
                    contenuto_richiesta.append("--- FINE DOCUMENTI ESEMPIO ---")

                # 3. FORZATURA JSON (Il trucco per far funzionare l'app)
                contenuto_richiesta.append("""
                ⚠️ ISTRUZIONE TECNICA FINALE ⚠️
                Rispondi ESCLUSIVAMENTE con un ARRAY JSON valido.
                Struttura obbligatoria:
                [
                    {
                        "domanda": "...",
                        "opzioni": ["A", "B", "C", "D"],
                        "corretta": 0,
                        "spiegazione": "..."
                    }
                ]
                """)

                # 4. CHIAMATA A GEMINI
                model = genai.GenerativeModel('gemini-3-flash-preview')
                response = model.generate_content(contenuto_richiesta)
                
                # 5. PARSING
                json_text = pulisci_json(response.text)
                st.session_state.quiz_data = json.loads(json_text)
                st.rerun()

            except Exception as e:
                st.error(f"Errore durante la generazione: {e}")
                st.error("Prova a ricaricare la pagina o controlla la tua connessione.")
    else:
        st.info("👈 Carica il documento di studio per iniziare.")

# --- FASE DI GIOCO (Rimasta uguale) ---
elif st.session_state.current_index < len(st.session_state.quiz_data):
    q = st.session_state.quiz_data[st.session_state.current_index]
    
    # Barra progresso
    prog = (st.session_state.current_index + 1) / len(st.session_state.quiz_data)
    st.progress(prog, text=f"Domanda {st.session_state.current_index + 1} di {len(st.session_state.quiz_data)}")
    
    st.subheader(q["domanda"])
    
    user_choice = st.radio("La tua risposta:", q["opzioni"], index=None, disabled=st.session_state.answer_submitted)
    col1, col2 = st.columns(2)
    
    if not st.session_state.answer_submitted:
        if col1.button("✅ Conferma"):
            if user_choice:
                st.session_state.answer_submitted = True
                st.rerun()
            else:
                st.warning("Devi scegliere una risposta!")
    else:
        correct_idx = q["corretta"]
        chosen_idx = q["opzioni"].index(user_choice) if user_choice in q["opzioni"] else -1
        
        if chosen_idx == correct_idx:
            st.success(f"Esatto! 🎉\n\n{q['spiegazione']}")
        else:
            st.error(f"Sbagliato. La risposta giusta era: {q['opzioni'][correct_idx]}")
            st.info(q['spiegazione'])
        
        if col2.button("Prossima ➡️"):
            if chosen_idx == correct_idx: st.session_state.score += 1
            st.session_state.answer_submitted = False
            st.session_state.current_index += 1
            st.rerun()

else:
    st.balloons()
    score = st.session_state.score
    total = len(st.session_state.quiz_data)
    perc = int(score/total * 100)
    st.title(f"Risultato: {score}/{total} ({perc}%)")
    
    if perc > 80: st.success("Grande! Sei pronto.")
    elif perc > 50: st.warning("Ripassa un po'.")
    else: st.error("Devi studiare di più.")
    
    if st.button("Ricomincia da capo"):
        st.session_state.quiz_data = None
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.answer_submitted = False
        st.rerun()