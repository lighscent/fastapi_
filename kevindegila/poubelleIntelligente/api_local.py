from fastapi import FastAPI, UploadFile
from tensorflow.keras.models import load_model
import numpy as np
import io
from PIL import Image
from contextlib import asynccontextmanager

model = None  # modèle global


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    # Chargement du modèle au démarrage
    model_path = (
        r"D:\\fastapi\\kevindegila\\2_DeepLearning_160\\CNN_Streamlit_APP\best_model.h5"
    )
    model = load_model(model_path, compile=False)
    yield
    # Ici tu peux ajouter du code de nettoyage à l’arrêt (si besoin)


app = FastAPI(lifespan=lifespan)


def preprocess(img):
    img = img.resize((224, 224))
    img = np.asarray(img)
    img = np.expand_dims(img, axis=0)
    return img


@app.get("/")
def great() -> dict:
    return {"message": "Bonjour 777"}


@app.post("/predict")
async def predict(file: UploadFile) -> dict:
    image_data = await file.read()
    img = Image.open(io.BytesIO(image_data))
    img_processed = preprocess(img)
    predictions = model.predict(img_processed)
    rec = predictions[0][0].tolist()
    return {"prediction": rec}
