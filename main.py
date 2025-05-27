import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# Inizializza OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Carica i CSV
df_vini = pd.read_csv("data/vini.csv")
df_piatti = pd.read_csv("data/piatti.csv")
df_vini.columns = df_vini.columns.str.strip()  # rimuove spazi

# Rinomina colonne per uniformità
df_vini = df_vini.rename(columns={"Nome Vino": "Nome"})
df_piatti = df_piatti.rename(columns={"Nome Piatto": "Nome"})

# Titolo
st.title("AI Sommelier per Ristoranti – Consigli Professionali")

# Selezione del piatto
piatto_selezionato = st.selectbox("Seleziona il piatto ordinato", df_piatti["Nome"])

# Selezione fascia di budget
fascia_budget = st.selectbox("Scegli la fascia di prezzo desiderata", [
    "Low budget (fino a 30€)",
    "Middle budget (31€ - 70€)",
    "High budget (oltre 70€)"
])

# Applica filtro prezzo
if fascia_budget == "Low budget (fino a 30€)":
    vini_filtrati = df_vini[df_vini["Prezzo"] <= 30]
elif fascia_budget == "Middle budget (31€ - 70€)":
    vini_filtrati = df_vini[(df_vini["Prezzo"] > 30) & (df_vini["Prezzo"] <= 70)]
else:
    vini_filtrati = df_vini[df_vini["Prezzo"] > 70]

# Se è stato selezionato un piatto e ci sono vini nel range
if piatto_selezionato and not vini_filtrati.empty:
    descrizione_piatto = df_piatti[df_piatti["Nome"] == piatto_selezionato]["Descrizione"].values[0]

    # Prepara lista vini per il prompt
    lista_vini = "\n".join(
        f"- {row['Nome']} ({row['Tipo']} - {row['Vitigno']}) - €{row['Prezzo']}"
        for _, row in vini_filtrati.iterrows()
    )

    # Prompt professionale
    prompt = f"""
Sei un sommelier esperto e professionale in un ristorante raffinato.
Un cliente ha ordinato il piatto: "{piatto_selezionato}" – {descrizione_piatto}.
Questi sono i vini disponibili nella fascia {fascia_budget}:

{lista_vini}

Scegli i 3 vini più adatti al piatto, assegna a ciascuno una percentuale di compatibilità e descrivili in modo professionale, convincente e chiaro. 
Ogni proposta deve invitare all'acquisto della bottiglia intera, sottolineando perché è una scelta ideale per il cliente.
"""

    # Richiesta all'AI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Sei un sommelier professionale, orientato alla vendita. Rispondi con competenza e stile sobrio ma coinvolgente."},
            {"role": "user", "content": prompt}
        ]
    )

    # Output
    st.markdown("### Proposte del sommelier:")
    st.write(response.choices[0].message.content)

elif piatto_selezionato and vini_filtrati.empty:
    st.warning("Nessun vino disponibile nella fascia di prezzo selezionata.")
