from fastapi import FastAPI, UploadFile

from tensorflow.keras.models import load_model
import numpy as np
import io
from PIL import Image

app = FastAPI()

# Ref.: https://www.youtube.com/watch?v=NhzqPSvT4A8

@app.get("/")
def great() -> dict:
    return {"message": "Bonjour 777"}


def load():
    model_path = "best_model.h5"
    model = load_model(model_path, compile=False)
    return model


def preprocess(img):
    img = img.resize((224, 224))
    img = np.asarray(img)
    img = np.expand_dims(img, axis=0)
    return img

# Chargement du model
model = load()


@app.post("/predict")
async def predict(file: UploadFile) -> dict:
    # lire le fichier image
    image_data = await file.read()

    # ouvrir l'image
    img = Image.open(io.BytesIO(image_data))

    # traitement de l'image
    img_processed = preprocess(img)

    # prediction
    predictions = model.predict(img_processed)
    rec = predictions[0][0].tolist()

    return {"prediction": rec}
