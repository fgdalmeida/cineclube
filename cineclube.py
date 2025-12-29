import streamlit as st
import pandas as pd
import random
import time
import os

# --- Banco de Dados ---
ARQUIVO = "filmes.csv"

def carregar():
    if os.path.exists(ARQUIVO):
        try:
            return pd.read_csv(ARQUIVO).to_dict('records')
        except:
            return []
    return []

def salvar(lista):
    pd.DataFrame(lista).to_csv(ARQUIVO, index=False)

# --- Configuração ---
st.set_page_config(page_title="Cine Clube", page_icon="🎬")

if 'movie_list' not in st.session_state:
    st.session_state.movie_list = carregar()

# --- Estilo ---
st.markdown("""
    <style>
    .vencedor { 
        padding: 20px; border-radius: 10px; border: 3px solid #E50914;
        background-color: #f0f2f6; text-align: center;
    }
    .filme-card {
        padding: 10px; background: white; border-radius: 5px;
        margin-bottom: 5px; border-left: 5px solid #E50914;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 Cine Clube")

# --- Cadastro ---
with st.expander("➕ Adicionar Novo Filme", expanded=True):
    c1, c2, c3 = st.columns(3)
    t = c1.text_input("Título")
    d = c2.text_input("Diretor")
    p = c3.text_input("Quem indicou?")
    
    if st.button("Salvar Filme"):
        if t and p:
            novo = {"titulo": t, "diretor": d if d else "N/A", "pessoa": p}
            st.session_state.movie_list.append(novo)
            salvar(st.session_state.movie_list)
            st.rerun()

# --- Lista e Sorteio ---
if st.session_state.movie_list:
    st.subheader(f"🍿 Filmes na disputa ({len(st.session_state.movie_list)})")
    
    for f in st.session_state.movie_list:
        st.markdown(f"""<div class='filme-card'><b>{f['titulo']}</b> ({f['diretor']})<br>
        <small>Indicado por: {f['pessoa']}</small></div>""", unsafe_allow_html=True)

    if st.button("🎲 SORTEAR AGORA", type="primary", use_container_width=True):
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)
        
        viciado = random.choice(st.session_state.movie_list)
        st.balloons()
        st.markdown(f"""<div class='vencedor'><h2>O escolhido foi...</h2>
        <h1 style='color: #E50914;'>{viciado['titulo']}</h1>
        <p>Direção: {viciado['diretor']} | Indicado por: {viciado['pessoa']}</p></div>""", unsafe_allow_html=True)
else:
    st.info("A lista está vazia!")

# --- Admin ---
st.sidebar.title("🔒 Admin")
senha = st.sidebar.text_input("Senha", type="password")
if senha == "pipoca":
    if st.sidebar.button("Limpar Lista"):
        st.session_state.movie_list = []
        if os.path.exists(ARQUIVO): os.remove(ARQUIVO)
        st.rerun()
