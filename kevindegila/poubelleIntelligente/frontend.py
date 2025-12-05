import streamlit as st
from PIL import Image
import requests

# Pour lancer
# streamlit run d:/fastapi/kevindegila/poubelleIntelligente/frontend.py 

# Vide les caches
# st.cache_data.clear()
# st.cache_resource.clear()

st.title("Poubelle Intelligente")

upload = st.file_uploader("Chargez l'image de votre objet", type=["png", "jpeg", "jpg"])

c1, c2 = st.columns(2)

if upload:
    files = {"file": upload.getvalue()}
    
    req = requests.post(
        "http://127.0.0.1:8000/predict", files=files
        # "https://fastapi-img-721899277959.europe-west1.run.app/predict", files=files
    )
    resultat = req.json()
    print(resultat)
    rec = resultat["prediction"]
    prob_recyclable = rec * 100
    prob_organic = (1 - rec) * 100

    c1.image(Image.open(upload))
    if prob_recyclable > 50:
        c2.write(
            f"Je suis certain à {prob_recyclable:.2f} % que l'objet est recyclable"
        )
    else:
        c2.write(
            f"Je suis certain à {prob_organic:.2f} % que l'objet n'est pas recyclable"
        )
