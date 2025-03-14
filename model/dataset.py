import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from ultralytics import YOLO
import numpy as np
from config import Config
from data_utils import extract_frames


class DangerousBehaviorDataset(Dataset):
    """
    危险行为数据集类
    """

    def __init__(self, video_paths, labels, transform=None):
        """
        初始化数据集

        Args:
            video_paths: 视频文件路径列表
            labels: 对应的标签列表
            transform: 图像变换
        """
        self.video_paths = video_paths
        self.labels = labels
        self.transform = transform

        # 初始化YOLOv8模型用于特征提取
        self.yolo = YOLO(Config.YOLO_MODEL)

    def __len__(self):
        """
        返回数据集大小
        """
        return len(self.video_paths)

    def extract_yolo_features(self, frames):
        """
        从帧序列中提取YOLOv8特征

        Args:
            frames: 帧列表

        Returns:
            features: 特征张量 [num_frames, feature_dim]
        """
        features = []
        for frame in frames:
            # 使用YOLOv8检测物体
            results = self.yolo(frame, verbose=False)

            # 提取检测到的对象特征
            if len(results) > 0 and len(results[0].boxes) > 0:
                # 获取检测框
                boxes = results[0].boxes.xyxy.cpu().numpy()
                # 获取置信度
                confs = results[0].boxes.conf.cpu().numpy()
                # 获取类别
                cls = results[0].boxes.cls.cpu().numpy()

                # 构建特征向量 (使用前10个检测框，如果不足则填充0)
                feature = np.zeros((10, 6))  # [x1, y1, x2, y2, conf, class]
                for i in range(min(10, len(boxes))):
                    feature[i, :4] = boxes[i]
                    feature[i, 4] = confs[i]
                    feature[i, 5] = cls[i]

                features.append(feature.flatten())
            else:
                # 如果没有检测到对象，则使用零向量
                features.append(np.zeros(10 * 6))

        return torch.tensor(features, dtype=torch.float32)

    def __getitem__(self, idx):
        """
        获取数据集中的一个样本

        Args:
            idx: 样本索引

        Returns:
            features: YOLOv8特征
            label: 对应的标签
        """
        video_path = self.video_paths[idx]
        label = self.labels[idx]

        # 从视频中提取帧
        frames = extract_frames(video_path, Config.SAMPLE_FRAMES)

        # 应用变换（如果有）
        if self.transform:
            frames = [self.transform(frame) for frame in frames]

        # 提取YOLOv8特征
        features = self.extract_yolo_features(frames)

        return features, torch.tensor(label, dtype=torch.long)


def get_data_loaders(dataset_splits):
    """
    创建数据加载器

    Args:
        dataset_splits: 包含训练、验证和测试集的字典

    Returns:
        字典包含训练、验证和测试数据加载器
    """
    # 定义数据变换
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # 创建数据集
    train_dataset = DangerousBehaviorDataset(
        dataset_splits['train']['videos'],
        dataset_splits['train']['labels'],
        transform
    )

    val_dataset = DangerousBehaviorDataset(
        dataset_splits['val']['videos'],
        dataset_splits['val']['labels'],
        transform
    )

    test_dataset = DangerousBehaviorDataset(
        dataset_splits['test']['videos'],
        dataset_splits['test']['labels'],
        transform
    )

    # 创建数据加载器
    train_loader = DataLoader(
        train_dataset,
        batch_size=Config.BATCH_SIZE,
        shuffle=True,
        num_workers=Config.NUM_WORKERS
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=Config.BATCH_SIZE,
        shuffle=False,
        num_workers=Config.NUM_WORKERS
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=Config.BATCH_SIZE,
        shuffle=False,
        num_workers=Config.NUM_WORKERS
    )

    return {
        'train': train_loader,
        'val': val_loader,
        'test': test_loader
    }


class RealTimeVideoDataset:
    """
    实时视频数据处理类，用于推理阶段
    """

    def __init__(self, transform=None):
        """
        初始化实时视频处理器

        Args:
            transform: 图像变换
        """
        self.transform = transform
        self.yolo = YOLO(Config.YOLO_MODEL)
        self.frame_buffer = []
        self.max_buffer_size = Config.SAMPLE_FRAMES

    def add_frame(self, frame):
        """
        添加一帧到缓冲区

        Args:
            frame: 输入帧
        """
        # 调整大小
        frame = cv2.resize(frame, Config.FRAME_SIZE)

        # 应用变换（如果有）
        if self.transform:
            frame = self.transform(frame)

        # 添加到缓冲区
        self.frame_buffer.append(frame)

        # 保持缓冲区大小不超过max_buffer_size
        if len(self.frame_buffer) > self.max_buffer_size:
            self.frame_buffer.pop(0)

    def get_features(self):
        """
        从缓冲区中获取特征

        Returns:
            features: YOLOv8特征
        """
        # 如果缓冲区不足，则返回None
        if len(self.frame_buffer) < self.max_buffer_size:
            return None

        features = []
        for frame in self.frame_buffer:
            # 使用YOLOv8检测物体
            results = self.yolo(frame, verbose=False)

            # 提取检测到的对象特征
            if len(results) > 0 and len(results[0].boxes) > 0:
                # 获取检测框
                boxes = results[0].boxes.xyxy.cpu().numpy()
                # 获取置信度
                confs = results[0].boxes.conf.cpu().numpy()
                # 获取类别
                cls = results[0].boxes.cls.cpu().numpy()

                # 构建特征向量 (使用前10个检测框，如果不足则填充0)
                feature = np.zeros((10, 6))  # [x1, y1, x2, y2, conf, class]
                for i in range(min(10, len(boxes))):
                    feature[i, :4] = boxes[i]
                    feature[i, 4] = confs[i]
                    feature[i, 5] = cls[i]

                features.append(feature.flatten())
            else:
                # 如果没有检测到对象，则使用零向量
                features.append(np.zeros(10 * 6))

        return torch.tensor(features, dtype=torch.float32).unsqueeze(0)  # 添加批次维度