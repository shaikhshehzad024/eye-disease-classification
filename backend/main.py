from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoImageProcessor, AutoModelForImageClassification
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load eye disease classifier
processor = AutoImageProcessor.from_pretrained("NeuronZero/EyeDiseaseClassifier")
model = AutoModelForImageClassification.from_pretrained("NeuronZero/EyeDiseaseClassifier")

# Load BLIP model for visual captioning
caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    # Classify eye disease
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    predicted_class_idx = outputs.logits.argmax(-1).item()
    label = model.config.id2label[predicted_class_idx]

    # Generate visual description
    caption_inputs = caption_processor(image, return_tensors="pt")
    with torch.no_grad():
        generated_ids = caption_model.generate(**caption_inputs)
    caption = caption_processor.decode(generated_ids[0], skip_special_tokens=True)

    # Combine into a dynamic report
    report = (
        f"The image appears to show: {caption}. "
        f"This is consistent with signs of **{label}** — "
        f"a condition that may require further medical evaluation."
    )

    return {
        "predicted_class": label,
        "generated_description": caption,
        "diagnosis_report": report
    }
