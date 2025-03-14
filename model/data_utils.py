import os
import cv2
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from config import Config
import glob
import random
import matplotlib.pyplot as plt


def get_video_paths(data_root):
    """
    获取数据目录中的所有视频文件路径及其标签

    Args:
        data_root: 数据集根目录，应包含各类别子目录

    Returns:
        video_paths: 视频文件路径列表
        labels: 对应的标签列表
    """
    video_paths = []
    labels = []

    # 遍历所有类别目录
    for class_id, class_name in Config.BEHAVIOR_CLASSES.items():
        class_dir = os.path.join(data_root, class_name)

        # 如果类别目录存在
        if os.path.isdir(class_dir):
            # 获取所有视频文件
            videos = glob.glob(os.path.join(class_dir, "*.mp4")) + \
                     glob.glob(os.path.join(class_dir, "*.avi")) + \
                     glob.glob(os.path.join(class_dir, "*.mov"))

            # 添加到列表
            video_paths.extend(videos)
            labels.extend([class_id] * len(videos))

    return video_paths, labels


def split_dataset(video_paths, labels):
    """
    将数据集划分为训练集、验证集和测试集

    Args:
        video_paths: 视频文件路径列表
        labels: 对应的标签列表

    Returns:
        字典包含训练、验证和测试数据
    """
    # 先划分出测试集
    train_val_videos, test_videos, train_val_labels, test_labels = train_test_split(
        video_paths, labels,
        test_size=Config.TEST_RATIO,
        random_state=42,
        stratify=labels
    )

    # 再划分训练集和验证集
    train_ratio_adjusted = Config.TRAIN_RATIO / (Config.TRAIN_RATIO + Config.VAL_RATIO)
    train_videos, val_videos, train_labels, val_labels = train_test_split(
        train_val_videos, train_val_labels,
        test_size=(1 - train_ratio_adjusted),
        random_state=42,
        stratify=train_val_labels
    )

    return {
        'train': {'videos': train_videos, 'labels': train_labels},
        'val': {'videos': val_videos, 'labels': val_labels},
        'test': {'videos': test_videos, 'labels': test_labels}
    }


def extract_frames(video_path, num_frames=16):
    """
    从视频中均匀提取指定数量的帧

    Args:
        video_path: 视频文件路径
        num_frames: 要提取的帧数量

    Returns:
        frames: 提取的帧列表，格式为RGB的NumPy数组
    """
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_indices = []

    # 如果视频帧数少于要提取的帧数
    if total_frames <= num_frames:
        frame_indices = list(range(total_frames))
    else:
        # 均匀采样
        frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)

    frames = []
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            # 转换为RGB格式
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 调整大小
            frame = cv2.resize(frame, Config.FRAME_SIZE)
            frames.append(frame)
        else:
            # 如果无法读取帧，使用黑色图像
            frames.append(np.zeros((Config.FRAME_SIZE[0], Config.FRAME_SIZE[1], 3), dtype=np.uint8))

    cap.release()
    return frames


def visualize_dataset_distribution(dataset_splits):
    """
    可视化数据集分布情况

    Args:
        dataset_splits: 包含训练、验证和测试集的字典
    """
    # 统计各类别在各数据集中的数量
    class_counts = {
        'train': np.zeros(Config.NUM_CLASSES),
        'val': np.zeros(Config.NUM_CLASSES),
        'test': np.zeros(Config.NUM_CLASSES)
    }

    for split_name, split_data in dataset_splits.items():
        for label in split_data['labels']:
            class_counts[split_name][label] += 1

    # 绘制柱状图
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(Config.NUM_CLASSES)
    width = 0.25

    ax.bar(x - width, class_counts['train'], width, label='Train')
    ax.bar(x, class_counts['val'], width, label='Validation')
    ax.bar(x + width, class_counts['test'], width, label='Test')

    ax.set_xticks(x)
    ax.set_xticklabels([Config.BEHAVIOR_CLASSES[i] for i in range(Config.NUM_CLASSES)])
    ax.set_xlabel('Behavior Classes')
    ax.set_ylabel('Count')
    ax.set_title('Dataset Distribution by Split')
    ax.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(Config.RESULT_DIR, 'dataset_distribution.png'))
    plt.close()