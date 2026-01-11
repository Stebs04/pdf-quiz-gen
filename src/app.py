import streamlit as st
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from utils import carica_file_su_gemini

# Carichiamo le variabili d'ambiente (per sviluppo locale)
load_dotenv()

# --- 1. CONFIGURAZIONE PAGINA E CSS PERSONALIZZATO ---
st.set_page_config(page_title="QuizGen AI", page_icon="🎓", layout="wide")

# Iniezione di CSS
st.markdown("""
<style>
    /* Sfondo generale */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Stile del bottone principale "Genera" */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #FF4B4B, #FF914D);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        font-weight: bold;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        border: 1px solid white;
    }

    /* Stile per le card delle domande */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    
    /* Barra di progresso personalizzata */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #00C9FF, #92FE9D);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. FUNZIONI HELPER (BACKEND) ---
def leggi_prompt(nome_file):
    """
    Legge i file di testo dalla cartella 'prompts'.
    Gestisce i percorsi in modo dinamico per funzionare sia su PC che su Cloud.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "prompts", nome_file)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "" # Ritorna stringa vuota se il file manca

def pulisci_json(testo_response):
    """
    Pulisce l'output dell'IA. Estrae solo la lista pura [ ... ].
    """
    testo_response = testo_response.replace("```json", "").replace("```", "")
    start = testo_response.find("[")
    end = testo_response.rfind("]") + 1
    if start != -1 and end != -1:
        return testo_response[start:end]
    return testo_response

# --- 3. GESTIONE STATO DELLA SESSIONE (MEMORIA) ---
if "quiz_data" not in st.session_state: st.session_state.quiz_data = None
if "current_index" not in st.session_state: st.session_state.current_index = 0
if "score" not in st.session_state: st.session_state.score = 0
if "answer_submitted" not in st.session_state: st.session_state.answer_submitted = False

# --- 4. CONFIGURAZIONE API ---
api_key = os.getenv("GOOGLE_API_KEY")

# Layout: Intestazione principale
col_logo, col_title = st.columns([1, 5])

with col_logo:
    st.markdown("<h1 style='text-align: center;'>🎓</h1>", unsafe_allow_html=True)

with col_title:
    st.title("Generatore di quiz")
    st.caption("Trasforma i tuoi PDF in simulazioni d'esame in 1 click.")

# Check API Key
if not api_key:
    st.warning("⚠️ Chiave API non trovata.")
    st.info("Crea un file .env o inserisci la chiave nei settings.")
    st.stop()

genai.configure(api_key=api_key)

# --- 5. SIDEBAR (INPUT UTENTE) ---
with st.sidebar:
    st.header("📂 I tuoi Materiali")
    
    # Upload del materiale di studio
    uploaded_file_studio = st.file_uploader(
        "1. Materiale di Studio (PDF/IMG)", 
        type=["pdf", "png", "jpg"], 
        key="studio"
    )
    
    st.markdown("---")
    
    # Upload degli esempi (Multiplo)
    uploaded_files_esempi = st.file_uploader(
        "2. Esempi (Opzionale)", 
        type=["pdf", "png", "jpg"], 
        key="esempi", 
        accept_multiple_files=True
    )
    
    st.markdown("---")
    
    # Bottone Reset (solo se c'è un quiz attivo)
    if st.session_state.quiz_data:
        if st.button("🔄 Resetta e Ricomincia"):
            st.session_state.quiz_data = None
            st.session_state.current_index = 0
            st.session_state.score = 0
            st.session_state.answer_submitted = False
            st.rerun()

# --- 6. LOGICA DI GENERAZIONE ---
if st.session_state.quiz_data is None:
    # Mostriamo la "Hero Section" se non c'è ancora un quiz
    if not uploaded_file_studio:
        st.info("👈 Carica il tuo PDF nella barra laterale per iniziare.")
    else:
        # Il bottone appare solo se c'è un file caricato
        if st.button("🚀 GENERA SIMULAZIONE D'ESAME", use_container_width=True):
            
            # Usiamo st.status per un feedback visivo moderno
            with st.status("🤖 L'IA sta lavorando...", expanded=True) as status:
                try:
                    # Step 1: Caricamento Prompt
                    st.write("Lettura istruzioni pedagogiche...")
                    p_base = leggi_prompt("base.txt")
                    p_style = leggi_prompt("style.txt")

                    # Step 2: Costruzione richiesta multimodale
                    req = []
                    req.append(p_base) # Istruzioni base
                    
                    st.write("Analisi visuale del documento di studio...")
                    file_studio_proc = carica_file_su_gemini(uploaded_file_studio)
                    req.append("--- INIZIO DOCUMENTO STUDIO ---")
                    req.append(file_studio_proc)
                    req.append("--- FINE DOCUMENTO STUDIO ---")

                    # Step 3: Aggiunta esempi stile (se presenti)
                    if uploaded_files_esempi:
                        st.write(f"Analisi di {len(uploaded_files_esempi)} file di esempio...")
                        req.append(p_style)
                        req.append("--- DOCUMENTI ESEMPIO ---")
                        for f in uploaded_files_esempi:
                            req.append(carica_file_su_gemini(f))
                    
                    # Step 4: Forzatura JSON (Cruciale per l'app)
                    req.append("""
                    ⚠️ OUTPUT TECNICO RICHIESTO ⚠️
                    Rispondi SOLO con un ARRAY JSON valido.
                    Struttura: [{"domanda": "...", "opzioni": ["A","B","C","D"], "corretta": 0, "spiegazione": "..."}]
                    Usa indice numerico per 'corretta' (0=A, 1=B...).
                    """)

                    # Step 5: Chiamata a Gemini
                    st.write("Generazione delle domande in corso...")
                    model = genai.GenerativeModel('gemini-3-flash-preview')
                    res = model.generate_content(req)
                    
                    # Parsing risultato
                    data = json.loads(pulisci_json(res.text))
                    st.session_state.quiz_data = data
                    
                    status.update(label="✅ Esame pronto!", state="complete", expanded=False)
                    st.rerun()

                except Exception as e:
                    st.error(f"Qualcosa è andato storto: {e}")
                    status.update(label="❌ Errore", state="error")

# --- 7. INTERFACCIA DI GIOCO (QUIZ) ---
elif st.session_state.current_index < len(st.session_state.quiz_data):
    
    # Recuperiamo i dati della domanda corrente
    q_data = st.session_state.quiz_data[st.session_state.current_index]
    total_q = len(st.session_state.quiz_data)
    current_q = st.session_state.current_index + 1
    
    # Barra di progresso
    st.progress(current_q / total_q, text=f"Domanda {current_q} di {total_q}")

    # Container per la domanda (effetto card)
    with st.container(border=True):
        st.subheader(f"Q{current_q}. {q_data['domanda']}")
        
        # Scelta risposta
        user_choice = st.radio(
            "Seleziona la risposta:", 
            q_data["opzioni"], 
            index=None, 
            disabled=st.session_state.answer_submitted,
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True) # Spaziatura
        
        col_actions = st.columns([1, 4])
        
        # Logica bottoni Conferma / Avanti
        if not st.session_state.answer_submitted:
            if col_actions[0].button("✅ Conferma"):
                if user_choice:
                    st.session_state.answer_submitted = True
                    st.rerun()
                else:
                    st.toast("⚠️ Seleziona una risposta prima!", icon="👆")
        else:
            # Calcolo correttezza
            correct_idx = q_data["corretta"]
            chosen_idx = q_data["opzioni"].index(user_choice) if user_choice in q_data["opzioni"] else -1
            is_correct = (chosen_idx == correct_idx)
            
            # Feedback visivo
            if is_correct:
                st.success(f"**Esatto!** 🎉\n\n{q_data['spiegazione']}")
            else:
                st.error(f"**Sbagliato.** La risposta giusta era: **{q_data['opzioni'][correct_idx]}**")
                st.info(f"💡 **Spiegazione:** {q_data['spiegazione']}")
            
            # Bottone Prossima Domanda
            if col_actions[0].button("Avanti ➡️"):
                if is_correct: st.session_state.score += 1
                st.session_state.answer_submitted = False
                st.session_state.current_index += 1
                st.rerun()

# --- 8. SCHERMATA RISULTATI ---
else:
    st.balloons()
    
    score = st.session_state.score
    total = len(st.session_state.quiz_data)
    perc = int((score / total) * 100)
    
    # Layout a colonne per i risultati
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.title("🏆 Esame Completato")
        st.metric(label="Il tuo Punteggio", value=f"{score}/{total}", delta=f"{perc}%")
        
        if perc >= 90:
            st.success("Risultato: ECCELLENTE (30 e Lode!) 🎓")
        elif perc >= 60:
            st.warning("Risultato: SUPERATO (Ma ripassa un po') 📚")
        else:
            st.error("Risultato: NON SUPERATO (Torna a studiare!) 🛑")
            
        if st.button("Ricomincia da capo", type="primary"):
            st.session_state.quiz_data = None
            st.session_state.current_index = 0
            st.session_state.score = 0
            st.session_state.answer_submitted = False
            st.rerun()