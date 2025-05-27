import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# Inizializza OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Carica i CSV
df_vini = pd.read_csv("data/vini.csv")
df_piatti = pd.read_csv("data/piatti.csv")

# Rinomina colonne per uniformità
df_vini = df_vini.rename(columns={
    "Nome Vino": "Nome"
})
df_piatti = df_piatti.rename(columns={"Nome Piatto": "Nome"})

# Titolo
st.title("AI Sommelier per Ristoranti – Consigli Professionali")

# Selezione del piatto e budget
piatto_selezionato = st.selectbox("Seleziona il piatto ordinato", df_piatti["Nome"])
budget = st.slider("Budget massimo per la bottiglia (€)", 10, 250, 60)

# Filtra vini per prezzo
vini_filtrati = df_vini[df_vini["Prezzo"] <= budget]

if piatto_selezionato and not vini_filtrati.empty:
    descrizione_piatto = df_piatti[df_piatti["Nome"] == piatto_selezionato]["Descrizione"].values[0]

    # Costruzione lista per il prompt
    lista_vini = "\n".join(
        f"- {row['Nome']} ({row['Tipo']} - {row['Vitigno']}) - €{row['Prezzo']}"
        for _, row in vini_filtrati.iterrows()
    )

    # Prompt orientato alla vendita
    prompt = f"""
Sei un sommelier professionale e competente. Un cliente ha ordinato il piatto: "{piatto_selezionato}" – {descrizione_piatto}.
Hai a disposizione questi vini:

{lista_vini}

Scegli i 3 vini più adatti al piatto, specifica per ciascuno una percentuale di compatibilità e spiega con stile elegante, convincente e professionale perché sono le scelte migliori.
Concludi ogni suggerimento con una frase che invogli il cliente ad acquistare la bottiglia.
"""

    # Richiesta all'AI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Sei un sommelier esperto, diretto e orientato alla vendita. Dai risposte eleganti e persuasive."},
            {"role": "user", "content": prompt}
        ]
    )

    # Output
    st.markdown("### Proposte del sommelier:")
    st.write(response.choices[0].message.content)
elif piatto_selezionato and vini_filtrati.empty:
    st.warning("Nessun vino disponibile entro il budget selezionato.")
