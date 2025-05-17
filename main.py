import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# Inizializza OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Carica il CSV
df = pd.read_csv("data/vini.csv")

# Titolo e input utente
st.title("AI Sommelier – Il tuo consigliere di vini")
user_input = st.text_input("Scrivi un piatto o un'occasione, e ti consiglierò un vino:")

# Filtri
tipologia = st.selectbox("Seleziona il tipo di vino", df["Tipologia"].unique())
gusto = st.selectbox("Scegli il gusto", df["Gusto"].unique())
vitigno = st.selectbox("Vitigno preferito", df["Vitigno"].unique())
budget = st.slider("Seleziona il budget massimo (€)", 5, 350, 50)

# Applica i filtri
filtrati = df[
    (df["Tipologia"] == tipologia) &
    (df["Gusto"] == gusto) &
    (df["Vitigno"] == vitigno) &
    (df["Prezzo"] <= budget)
]

# Costruisci il prompt in base ai risultati
if user_input:
    if not filtrati.empty:
        vino = filtrati.sample(1).iloc[0]
        prompt = (
            f"L'utente cerca un vino per '{user_input}'. Consiglia questo vino: "
            f"{vino['Nome']} ({vino['Regione']}, {vino['Nazione']}) - "
            f"Tipologia: {vino['Tipologia']}, Vitigno: {vino['Vitigno']}, "
            f"Gusto: {vino['Gusto']}, prezzo: {vino['Prezzo']}€, ideale per: {vino['Abbinamento']}."
        )
    else:
        prompt = (
            f"L'utente cerca un vino per '{user_input}', ma non ci sono risultati con "
            f"Tipologia: {tipologia}, Gusto: {gusto}, Vitigno: {vitigno}, Budget massimo: {budget}€. "
            "Spiega gentilmente che non ci sono abbinamenti perfetti e suggerisci alternative generiche."
        )

    # Richiesta a OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Sei un sommelier esperto italiano. Dai consigli professionali ma chiari."},
            {"role": "user", "content": prompt}
        ]
    )

    # Output
    st.markdown("### Consiglio del sommelier:")
    st.write(response.choices[0].message.content)
