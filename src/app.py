import streamlit as st
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from utils import carica_file_su_gemini

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

# --- LOGIN ---
def check_password():
    password_segreta = os.getenv("APP_PASSWORD")
    if not password_segreta: return True
    if st.session_state.get("authenticated", False): return True

    pwd = st.sidebar.text_input("🔒 Password:", type="password")
    if pwd == password_segreta:
        st.session_state["authenticated"] = True
        st.rerun()
    elif pwd:
        st.sidebar.error("Errata ❌")
    return False

# --- SESSION STATE ---
if "quiz_data" not in st.session_state: st.session_state.quiz_data = None
if "current_index" not in st.session_state: st.session_state.current_index = 0
if "score" not in st.session_state: st.session_state.score = 0
if "answer_submitted" not in st.session_state: st.session_state.answer_submitted = False

api_key = os.getenv("GOOGLE_API_KEY")

if check_password():
    st.title("🎮 Quiz Interattivo Universitario")

    if not api_key:
        st.error("Manca la API Key nel file .env")
        st.stop()
    
    genai.configure(api_key=api_key)

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("📂 Input")
        uploaded_file_studio = st.file_uploader("1. Documento Studio", type=["pdf", "png", "jpg"], key="studio")
        st.markdown("---")
        uploaded_file_esempi = st.file_uploader("2. Esempio Stile (Opzionale)", type=["pdf", "png", "jpg"], key="esempi")
        st.markdown("---")
        
        if st.button("🚀 Genera Nuovo Quiz", type="primary"):
            st.session_state.quiz_data = None
            st.session_state.current_index = 0
            st.session_state.score = 0
            st.session_state.answer_submitted = False
            st.rerun()

    # --- LOGICA ---
    if st.session_state.quiz_data is None:
        if uploaded_file_studio:
            with st.spinner("🧠 Sto leggendo i file di prompt e analizzando il documento..."):
                try:
                    # 1. CARICHIAMO I PROMPT DAI FILE DI TESTO
                    prompt_base_text = leggi_prompt("base.txt")
                    prompt_style_text = leggi_prompt("style.txt")

                    # 2. COSTRUIAMO LA LISTA PER GEMINI
                    contenuto_richiesta = []
                    
                    # Aggiungiamo il prompt base (Docente Esperto...)
                    contenuto_richiesta.append(prompt_base_text)

                    # Aggiungiamo il documento di studio
                    st.text("Upload documento studio...")
                    file_studio_proc = carica_file_su_gemini(uploaded_file_studio)
                    contenuto_richiesta.append("--- INIZIO DOCUMENTO STUDIO ---")
                    contenuto_richiesta.append(file_studio_proc)
                    contenuto_richiesta.append("--- FINE DOCUMENTO STUDIO ---")

                    # Aggiungiamo esempi e prompt di stile (se presenti)
                    if uploaded_file_esempi:
                        st.text("Upload documento esempi...")
                        file_esempi_proc = carica_file_su_gemini(uploaded_file_esempi)
                        # Qui inseriamo il testo letto da style.txt
                        contenuto_richiesta.append(prompt_style_text)
                        contenuto_richiesta.append(file_esempi_proc)

                    # 3. OVERRIDE JSON (FONDAMENTALE)
                    # Anche se il file di testo chiede un output formattato per umani,
                    # noi forziamo Gemini a darci JSON per far funzionare l'app.
                    contenuto_richiesta.append("""
                    
                    ⚠️ ISTRUZIONE TECNICA PRIORITARIA ⚠️
                    Indipendentemente dal formato richiesto sopra, DEVI rispondere 
                    ESCLUSIVAMENTE con un ARRAY JSON valido per permettere al software di funzionare.
                    
                    Struttura JSON obbligatoria:
                    [
                        {
                            "domanda": "...",
                            "opzioni": ["A", "B", "C", "D"],
                            "corretta": 0,  <-- (Int: 0=A, 1=B, 2=C, 3=D)
                            "spiegazione": "..."
                        }
                    ]
                    """)

                    # 4. Chiamata a Gemini
                    model = genai.GenerativeModel('gemini-3-flash-preview')
                    response = model.generate_content(contenuto_richiesta)
                    
                    json_text = pulisci_json(response.text)
                    st.session_state.quiz_data = json.loads(json_text)
                    st.rerun()

                except Exception as e:
                    st.error(f"Errore: {e}")
        else:
            st.info("👈 Carica i documenti per iniziare.")

    # --- GIOCO INTERATTIVO (Uguale a prima) ---
    elif st.session_state.current_index < len(st.session_state.quiz_data):
        q = st.session_state.quiz_data[st.session_state.current_index]
        st.progress((st.session_state.current_index + 1) / len(st.session_state.quiz_data), text=f"Domanda {st.session_state.current_index + 1}")
        st.subheader(q["domanda"])
        
        user_choice = st.radio("Scegli:", q["opzioni"], index=None, disabled=st.session_state.answer_submitted)
        col1, col2 = st.columns(2)
        
        if not st.session_state.answer_submitted:
            if col1.button("✅ Conferma"):
                if user_choice:
                    st.session_state.answer_submitted = True
                    st.rerun()
                else:
                    st.warning("Seleziona una risposta!")
        else:
            correct_idx = q["corretta"]
            chosen_idx = q["opzioni"].index(user_choice) if user_choice in q["opzioni"] else -1
            
            if chosen_idx == correct_idx:
                st.success(f"Esatto! 🎉\n\n{q['spiegazione']}")
            else:
                st.error(f"Sbagliato. Risposta giusta: {q['opzioni'][correct_idx]}")
                st.info(f"{q['spiegazione']}")
            
            if col2.button("Avanti ➡️"):
                if chosen_idx == correct_idx: st.session_state.score += 1
                st.session_state.answer_submitted = False
                st.session_state.current_index += 1
                st.rerun()

    else:
        st.balloons()
        score = st.session_state.score
        total = len(st.session_state.quiz_data)
        st.title(f"Punteggio: {score}/{total}")
        if st.button("Ricomincia"):
            st.session_state.quiz_data = None
            st.session_state.current_index = 0
            st.session_state.score = 0
            st.session_state.answer_submitted = False
            st.rerun()