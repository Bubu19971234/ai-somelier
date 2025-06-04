import streamlit as st
import pandas as pd
import os
import re
from openai import OpenAI

# Inizializza OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Carica CSV
df_vini = pd.read_csv("data/vini.csv")
df_piatti = pd.read_csv("data/piatti.csv")
df_vini.columns = df_vini.columns.str.strip()
df_vini = df_vini.rename(columns={"Nome Vino": "Nome"})
df_piatti = df_piatti.rename(columns={"Nome Piatto": "Nome"})

# STILE CSS
st.markdown("""
    <style>
    html, body, .main {
        background-color: white;
        color: black;
    }
    .block-container {
        padding-top: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    .gradient-title {
        font-size: 36px;
        font-weight: bold;
        background: linear-gradient(to right, #d3d3d3, #c0c0c0, #6b0f1a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 10px;
    }
    .wine-box {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: #fafafa;
    }
    .wine-title {
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .compatibility-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 50px;
        font-weight: bold;
        color: white;
        margin-top: 5px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Titolo con gradiente
st.markdown('<div class="gradient-title">AI Sommelier per Ristoranti</div>', unsafe_allow_html=True)

# Selezione numero di partecipanti e piatti
numero_commensali = st.slider("ð¥ Quanti siete a cena?", 1, 6, 2)

piatti_selezionati = []
for i in range(numero_commensali):
    piatto = st.selectbox(f"Piatto partecipante {i+1}", df_piatti["Nome"].tolist(), key=f"piatto_{i}")
    piatti_selezionati.append(piatto)

# Fascia di prezzo
fascia_budget = st.selectbox("Scegli la fascia di prezzo desiderata", [
    "Low budget (fino a 30â¬)",
    "Middle budget (31â¬ - 70â¬)",
    "High budget (oltre 70â¬)"
])

if fascia_budget == "Low budget (fino a 30â¬)":
    vini_filtrati = df_vini[df_vini["Prezzo"] <= 30]
elif fascia_budget == "Middle budget (31â¬ - 70â¬)":
    vini_filtrati = df_vini[(df_vini["Prezzo"] > 30) & (df_vini["Prezzo"] <= 70)]
else:
    vini_filtrati = df_vini[df_vini["Prezzo"] > 70]

def get_color(score):
    if score >= 80:
        return "#4CAF50"
    elif 50 <= score < 80:
        return "#FFC107"
    else:
        return "#F44336"

def mostra_vino(titolo, compat, testo):
    colore = get_color(compat)
    st.markdown(f"""
        <div class="wine-box">
            <div class="wine-title">{titolo}</div>
            <div class="compatibility-badge" style="background-color:{colore}">
                CompatibilitÃ : {compat}%
            </div>
            <div>{testo}</div>
        </div>
    """, unsafe_allow_html=True)

# Bottone per attivare ricerca
if st.button("ð· Consigliami"):
    if piatti_selezionati and not vini_filtrati.empty:
        descrizioni = []
        for piatto in piatti_selezionati:
            riga = df_piatti[df_piatti["Nome"] == piatto]
            if not riga.empty:
                descrizioni.append(f"\"{piatto}\" â {riga['Descrizione'].values[0]}")
        descrizione_completa = "\n".join(descrizioni)

        lista_vini = "\n".join(
            f"- {row['Nome']} ({row['Tipo']} - {row['Vitigno']}) - â¬{row['Prezzo']}"
            for _, row in vini_filtrati.iterrows()
        )

        prompt = f"""Sei un sommelier esperto. Un gruppo ha ordinato questi piatti:\n
{descrizione_completa}\n
Questi sono i vini disponibili nella fascia {fascia_budget}:\n
{lista_vini}\n
Consiglia 3 vini adatti allâinsieme dei piatti. Per ogni vino, indica:
- Nome
- CompatibilitÃ  in percentuale
- Una descrizione coinvolgente e orientata alla vendita della bottiglia intera.
"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Sei un sommelier professionale, orientato alla vendita. Rispondi con competenza e stile sobrio ma coinvolgente."},
                {"role": "user", "content": prompt}
            ]
        )

        st.markdown("### ð§  Proposte del sommelier per il tavolo:")
        output = response.choices[0].message.content.split("\n\n")
        for blocco in output:
            if "%" in blocco:
                righe = blocco.strip().split("\n")
                nome = righe[0].strip()
                percentuale = next((int(re.search(r'\\d+', s).group()) for s in righe if '%' in s), 0)
                descrizione = " ".join(righe[1:])
                mostra_vino(nome, percentuale, descrizione)

    elif piatti_selezionati and vini_filtrati.empty:
        st.warning("Nessun vino disponibile nella fascia di prezzo selezionata.")
