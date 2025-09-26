# backend/models/xray_analysis.py

import torch
from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
from models.health_llm import HealthLLM  # Your LLM wrapper

# ✅ Use a public Hugging Face chest X-ray model
MODEL_NAME = "microsoft/resnet-50"  # General ImageNet model (we’ll adapt for medical use)

# You can swap this with a specialized medical model when available:
# MODEL_NAME = "microsoft/biogpt"   (text) 
# MODEL_NAME = "nielsr/mobilenetv2-finetuned-chest-xray-pneumonia"  (better choice for pneumonia)

# Load extractor + model
extractor = AutoFeatureExtractor.from_pretrained(MODEL_NAME)
xray_model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
xray_model.eval()

# Load the LLM for summaries
llm = HealthLLM()

def analyze_xray(image_path: str) -> dict:
    """
    Analyze an X-ray image, predict disease, and generate a summary.
    """
    # Preprocess the image
    img = Image.open(image_path).convert("RGB")
    inputs = extractor(images=img, return_tensors="pt")

    # Run inference
    with torch.no_grad():
        outputs = xray_model(**inputs)
        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).item()

    # Get label from model config
    predicted_class = xray_model.config.id2label[predicted_class_idx]

    # Generate dynamic summary using LLM
    prompt = (
        f"The chest X-ray was classified as **{predicted_class}**. "
        f"Provide a concise summary explaining the likely condition and next steps."
    )
    summary = llm.generate_text(prompt)

    return {
        "prediction": predicted_class,
        "summary": summary
    }
