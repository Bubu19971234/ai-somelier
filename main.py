import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# Inizializza OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Carica i CSV da /data/
df_vini = pd.read_csv("data/vini.csv")
df_piatti = pd.read_csv("data/piatti.csv")

# Interfaccia
st.title("Sommelier Digitale per Ristoranti")

# Dropdown piatti
piatto_selezionato = st.selectbox("Seleziona il piatto ordinato", df_piatti["Nome Piatto"])
# Budget
budget = st.slider("Budget massimo per la bottiglia (€)", 10, 250, 60)

# Filtra vini per prezzo
vini_filtrati = df_vini[df_vini["Prezzo"] <= budget]

if piatto_selezionato:
descrizione_piatto = df_piatti[df_piatti["Nome Piatto"] == piatto_selezionato]["Descrizione"].values[0]
    # Prepara lista vini formattata per prompt
    lista_vini = "\n".join(
        f"- {row['Nome vino']} ({row['Tipo']}, {row['Vitigno']}), €{row['Prezzo (€)']}: {row['Descrizione']}"
        for _, row in vini_filtrati.iterrows()
    )

    # Prompt poetico
    prompt = f"""
Agisci come un sommelier esperto ed elegante in una raffinata enoteca italiana.
Un cliente ha appena ordinato: "{piatto_selezionato}" – {descrizione_piatto}.
Tra i vini disponibili oggi nel ristorante:

{lista_vini}

Scegli un solo vino perfetto da abbinare e raccontalo con toni poetici, evocativi, persuasivi.
Non elencare: narra. Descrivi l'emozione dell'abbinamento, le sfumature. 
Concludi sempre con una frase che inviti il cliente ad acquistare la bottiglia intera.
"""

    # Richiesta a OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Sei un sommelier appassionato e teatrale. Dai consigli coinvolgenti e raffinati."},
            {"role": "user", "content": prompt}
        ]
    )

    # Risultato
    st.markdown("### Consiglio del sommelier:")
    st.write(response.choices[0].message.content)
