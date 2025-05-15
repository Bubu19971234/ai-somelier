from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
import streamlit as st

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
import pandas as pd

# Carica il file CSV
df = pd.read_csv("data/vini.csv")

# Filtri utente
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
    vino = filtrati.sample(1).iloc[0]  # Sceglie un vino a caso tra quelli filtrati
    prompt = f"Consiglia questo vino per {vino['Occasione']}: {vino['Nome']} ({vino['Regione']}, {vino['Nazione']}, {vino['Prezzo']}€). Abbinamenti ideali: {vino['Abbinamento']}."
else:
    prompt = "Non ho trovato un vino che rispecchi tutti i tuoi criteri. Vuoi rilanciare la ricerca con meno filtri?"

st.title("AI Sommelier – Il tuo consigliere di vini")

user_input = st.text_input("Scrivi un piatto o un'occasione, e ti consiglierò un vino:")

if user_input:
    import openai
    openai.api_key = os.environ["OPENAI_API_KEY"]

    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Sei un sommelier italiano esperto. Consiglia vini perfetti per ogni piatto o occasione, con spiegazioni semplici e professionali."},
        {"role": "user", "content": user_input}
        # Mostra il consiglio o un messaggio se non trovato
if not filtrati.empty:
    vino = filtrati.sample(1).iloc[0]
    prompt = (
        f"Consiglia questo vino per l'occasione '{vino['Occasione']}': "
        f"{vino['Nome']} ({vino['Regione']}, {vino['Nazione']}, {vino['Vitigno']}, "
        f"{vino['Gusto']}, {vino['Tipologia']}, €{vino['Prezzo']}) "
        f"abbinato a {vino['Abbinamento']}."
    )
else:
    prompt = "Non ho trovato un vino che rispecchi tutti i tuoi criteri. Vuoi rilanciare la ricerca?"

st.title("AI Sommelier – Il tuo consigliere di vini")
user_input = st.text_input("Scrivi un piatto o un'occasione, e ti consiglierò un vino:")

if user_input:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Sei un sommelier italiano esperto. Consiglia vini perfetti per ogni piatto o occasione, con spiegazioni semplici e professionali.",
            },
            {"role": "user", "content": user_input + "\n" + prompt}
        ]
    )

    st.markdown("### Consiglio del sommelier:")
    st.write(response.choices[0].message.content)
    ]
)

st.markdown("### Consiglio del sommelier:")
st.write(response.choices[0].message.content)
