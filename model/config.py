import torch
import os


class Config:
    # 路径配置
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    DATA_ROOT = os.path.join(PROJECT_ROOT, "data")
    MODEL_SAVE_DIR = os.path.join(PROJECT_ROOT, "saved_models")
    LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
    RESULT_DIR = os.path.join(PROJECT_ROOT, "results")

    # 创建必要的目录
    os.makedirs(DATA_ROOT, exist_ok=True)
    os.makedirs(MODEL_SAVE_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(RESULT_DIR, exist_ok=True)

    # 数据集配置
    TRAIN_RATIO = 0.7
    VAL_RATIO = 0.15
    TEST_RATIO = 0.15

    # 视频帧配置
    SAMPLE_FRAMES = 16  # 每个视频片段采样的帧数
    FRAME_SIZE = (224, 224)  # 调整帧大小

    # YOLOv8配置
    YOLO_MODEL = "yolov8n.pt"  # 可选: yolov8n.pt, yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt
    CONFIDENCE_THRESHOLD = 0.5  # 检测置信度阈值

    # 危险行为类别
    BEHAVIOR_CLASSES = {
        0: "normal",  # 正常行为
        1: "fighting",  # 打架
        2: "robbery",  # 抢劫
        3: "vandalism",  # 破坏公物
        4: "arson",  # 纵火
        5: "explosion",  # 爆炸
        6: "assault",  # 袭击
        7: "shooting",  # 枪击
        8: "shoplifting",  # 偷窃
        9: "burglary"  # 入室盗窃
    }
    NUM_CLASSES = len(BEHAVIOR_CLASSES)

    # LSTM模型配置
    YOLO_FEATURE_SIZE = 60  # YOLOv8特征向量大小 (10个框 × 6个特征)
    LSTM_HIDDEN_SIZE = 256
    LSTM_NUM_LAYERS = 2
    DROPOUT_RATE = 0.5

    # 训练参数
    BATCH_SIZE = 8
    NUM_EPOCHS = 30
    LEARNING_RATE = 0.001
    WEIGHT_DECAY = 1e-5
    EARLY_STOPPING_PATIENCE = 5

    # 设备配置
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    NUM_WORKERS = 4  # DataLoader工作线程数
