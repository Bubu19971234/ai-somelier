import openai
import streamlit as st

import os
openai.api_key = os.environ["OPENAI_API_KEY"]

st.title("AI Sommelier – Il tuo consigliere di vini")

user_input = st.text_input("Scrivi un piatto o un'occasione, e ti consiglierò un vino:")

if user_input:
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Sei un sommelier italiano esperto. Consiglia vini perfetti per ogni piatto o occasione, con spiegazioni semplici e professionali."},
            {"role": "user", "content": user_input}
        ]
    )
    st.markdown("### Consiglio del sommelier:")
    st.write(response.choices[0].message["content"])
