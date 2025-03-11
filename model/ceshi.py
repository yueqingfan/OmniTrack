import torch
import clip
from PIL import Image

# 设备选择：如果有GPU，优先使用
device = "cuda" if torch.cuda.is_available() else "cpu"

# 加载 ViT-L/14@336px CLIP 模型
model, preprocess = clip.load("ViT-L/14@336px", device=device)

# 读取并预处理测试图片
image_path = "WIN_20250310_22_54_02_Pro.jpg"  # 替换为你的测试图片路径
image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)

# 定义测试标签
labels = [
    "a scene of fire or burning",
    "a young boy standing",
    "a severe car crash or accident",
    "a violent fight between people",
    "people engaged in normal daily activities",
    "a group of people",
]

# 处理文本输入
text_inputs = clip.tokenize(labels).to(device)

# 进行推理
with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text_inputs)

    # 计算相似度（归一化余弦相似度）
    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)
    similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)

# 获取预测结果
pred_index = similarity.argmax().item()
pred_label = labels[pred_index]
pred_confidence = similarity[0, pred_index].item()

# 输出结果
print(f"Predicted Label: {pred_label}, Confidence: {pred_confidence:.4f}")
