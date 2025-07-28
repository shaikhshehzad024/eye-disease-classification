from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

processor = AutoImageProcessor.from_pretrained("NeuronZero/EyeDiseaseClassifier")
model = AutoModelForImageClassification.from_pretrained("NeuronZero/EyeDiseaseClassifier")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    predicted_class_idx = outputs.logits.argmax(-1).item()
    label = model.config.id2label[predicted_class_idx]

    return {"predicted_class": label}

# uvicorn main:app --reload --port 8000
