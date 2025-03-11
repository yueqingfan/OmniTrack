from fastapi import FastAPI, UploadFile, File
import clip
import torch
from PIL import Image
import io

app = FastAPI()
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-L/14@336px", device=device)

@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    image_bytes = await image.read()
    image = Image.open(io.BytesIO(image_bytes))
    image = preprocess(image).unsqueeze(0).to(device)

    labels = [
        'normal',
        'people fighting on a street',
        'fire on a street',
        'street violence or rioting',
        'serious car crash',
        'hit-and-run incident',
        'aggressive driving or road rage',
        'person brandishing a weapon',
        'armed robbery in public',
        'sudden large crowd gathering',
        'suspicious abandoned object',
        'explosion on a street',
        'violence in an office',
        'fire breaking out in an office',
        'gun violence in a building',
        'hostage situation',
        'sudden panic or evacuation',
        'person trespassing in a restricted area',
        'theft or unauthorized access',
        'suspicious behavior in an office',
        'arson attempt indoors',
        'arrest in progress',
        'physical assault or abuse',
        'gun shooting incident',
        'explosion occurring',
        'burglary or forced entry',
        'looting or large-scale theft',
        'vandalism or property destruction',
        'dangerous road accident',
        'suspicious package left unattended',
        'violent protest or mob activity'
    ]

    text_inputs = clip.tokenize(labels).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text_inputs)
        similarity = (image_features @ text_features.T).softmax(dim=-1)

    best_idx = similarity.argmax().item()
    return {"label": labels[best_idx], "confidence": similarity[0, best_idx].item()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
