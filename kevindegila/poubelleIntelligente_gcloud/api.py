import datetime, io, os
from fastapi import FastAPI, UploadFile


os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from google.cloud import storage
from dotenv import load_dotenv

# Chargere les variables d'envirronement
load_dotenv()
bucket_name = os.getenv("BUCKET_NAME")
json_key = os.getenv("JSON_KEY")

app = FastAPI()


def save_to_gcs(content, filename):
    # Initialiser le client GCS avec le fichier de clé JSON
    storage_client = storage.Client.from_service_account_json(json_key)

    # Récupérer le bucket
    bucket = storage_client.bucket(bucket_name)

    # Créer un nouveau blob (fichier) dans le bucket
    destination = f"images/{filename}"
    blob = bucket.blob(destination)

    # Uploader le contenu dans le blob
    blob.upload_from_string(content, content_type="image/jpeg")

    print(f"Fichier {destination} uploadé dans le bucket {bucket_name}.")


@app.get("/")
def great():
    return {"message": "Bonjour API"}


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
async def predict(file: UploadFile):
    # lire le fichier image
    image_data = await file.read()

    # ouvrir l'image
    img = Image.open(io.BytesIO(image_data))

    # traitement de l'image
    img_processed = preprocess(img)

    # prediction
    predictions = model.predict(img_processed)
    rec = predictions[0][0].tolist()

    # upload les images
    current_time = datetime.datetime.now()
    time_string = current_time.strftime("%Y%m%d %H%M%S")

    filename = f"{time_string}_proba_{str(rec)}.jpeg"
    save_to_gcs(image_data, filename)

    return {"prediction": rec}
