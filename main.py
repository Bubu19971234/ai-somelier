from openai import OpenAI
import os
import streamlit as st
import pandas as pd

# Chiave API da variabile ambiente
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Carica il file CSV
df = pd.read_csv("data/vini.csv")

# Filtri utente
st.title("AI Sommelier – Il tuo consigliere di vini")

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

# Mostra il consiglio o un messaggio se non trovato
if not filtrati.empty:
    vino = filtrati.sample(1).iloc[0]
    prompt = (
        f"Consiglia questo vino per l'occasione '{vino['Occasione']}': "
        f"{vino['Nome']}, {vino['Regione']}, {vino['Nazione']}, {vino['Vitigno']}, "
        f"{vino['Gusto']}, {vino['Tipologia']}, {vino['Prezzo']}€, "
        f"abbinato a {vino['Abbinamento']}."
    )
else:
    prompt = "Non ho trovato un vino che rispecchi tutti i tuoi criteri. Vuoi rilanciare la ricerca con filtri diversi?"

# Input libero dell'utente
user_input = st.text_input("Scrivi un piatto o un'occasione, e ti consiglierò un vino:")

if user_input:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Sei un sommelier italiano esperto. Consiglia vini con spiegazioni semplici e professionali."},
            {"role": "user", "content": f"{prompt}\nDomanda: {user_input}"}
        ]
    )
    st.markdown("### Consiglio del sommelier:")
st.write(response.choices[0].message.content)
