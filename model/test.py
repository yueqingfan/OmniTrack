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
        "normal",

        # 虐待 (Abuse)
        "physical abuse in a domestic setting",
        "child abuse incident captured on video",
        "elder abuse in a care facility",
        "domestic violence with visible injuries",

        # 火灾 (Fire)
        "fire spreading across building",
        "building burning with heavy smoke",
        "flames consuming structure",
        "smoke billowing from burning site",
        "house fire with active flames",

        # 打架 (Fighting)
        "violent physical confrontation",
        "people throwing punches at each other",
        "aggressive physical altercation between individuals",
        "people engaged in fistfight",
        "violent brawl with pushing and shoving",
        "crowd fight with multiple participants",
        "street fight with physical violence",
        "bar fight with aggressive combat",
        "public physical altercation",
        "group fighting with chaotic movements",
        "Two people are fighting",
        "A group of people are fighting",

        # 盗窃 (Theft)
        "theft incident in a public area",
        "pickpocketing event in a crowded location",
        "burglary with forced entry at night",
        "shoplifting captured in a retail store",
        "robbery confrontation with visible threat",

        # 爆炸 (Explosion)
        "explosion incident in an urban environment",
        "bomb explosion with a visible shockwave",
        "industrial explosion with debris and fire",
        "sudden explosion in a public venue",

        # 枪击 (Shooting)
        "gun shooting incident in a crowded area",
        "active shooter scenario with police response",
        "mass shooting event with multiple casualties",
        "urban shooting scene with visible gunfire"
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