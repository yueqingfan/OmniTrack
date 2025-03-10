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
        # 户外场景
        'people walking on a street',
        'buildings',
        'fight on a street',
        'fire on a street',
        'street violence',
        'road',
        'car crash',
        'cars on a road',
        'car parking area',
        'cars',

        # 室内场景
        'office environment',
        'office corridor',
        'violence in office',
        'fire in office',
        'people talking',
        'people walking in office',
        'person walking in office',
        'group of people',

        # UCF-Crime 异常行为
        'arrest happening',
        'assault or physical violence',
        'fighting between people',
        'abuse or mistreatment',
        'gun shooting',
        'explosion occurring',
        'arson or setting fire',
        'burglary or breaking into a house',
        'robbery happening in public',
        'shoplifting in a store',
        'stealing an object or item',
        'vandalism or damaging property',
        'serious road accident',

        # 其他正常行为
        'a peaceful street',
        'a normal office environment',
        'a person standing still',
        'a person sitting quietly',
        'an empty office',
        'an empty street'
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
