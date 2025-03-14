import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
import numpy as np
import time
import os
from tqdm import tqdm
import logging
from datetime import datetime

from config import Config
from data_utils import get_video_paths, split_dataset, visualize_dataset_distribution
from dataset import get_data_loaders
from models import YOLOLSTM, YOLOLSTMv2
from utils import EarlyStopping, plot_confusion_matrix, save_classification_report, plot_training_history, \
    calculate_metrics


def setup_logger():
    """
    设置日志记录器
    """
    # 创建logger
    logger = logging.getLogger('dangerous_behavior_detection')
    logger.setLevel(logging.INFO)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 创建文件处理器
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(Config.LOG_DIR, f'training_{current_time}.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 添加处理器到logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def train():
    """
    训练模型
    """
    # 设置日志记录器
    logger = setup_logger()
    logger.info("Starting training process...")

    # 设置随机种子
    torch.manual_seed(42)
    np.random.seed(42)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(42)

    # 获取数据
    logger.info("Loading data...")
    video_paths, labels = get_video_paths(Config.DATA_ROOT)
    dataset_splits = split_dataset(video_paths, labels)

    # 可视化数据集分布
    visualize_dataset_distribution(dataset_splits)

    # 获取数据加载器
    logger.info("Preparing data loaders...")
    data_loaders = get_data_loaders(dataset_splits)

    # 创建模型
    logger.info("Creating model...")
    # model = YOLOLSTM()  # 使用基础模型
    model = YOLOLSTMv2()  # 使用改进模型
    model = model.to(Config.DEVICE)

    # 定义损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=Config.LEARNING_RATE, weight_decay=Config.WEIGHT_DECAY)

    # 学习率调度器
    scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3, verbose=True)

    # 早停
    model_save_path = os.path.join(Config.MODEL_SAVE_DIR, 'best_model.pth')
    early_stopping = EarlyStopping(patience=Config.EARLY_STOPPING_PATIENCE, verbose=True, path=model_save_path)

    # 训练历史
    history = {
        'train_loss': [],
        'val_loss': [],
        'train_acc': [],
        'val_acc': []
    }

    # 训练循环
    logger.info("Starting training loop...")
    start_time = time.time()

    for epoch in range(Config.NUM_EPOCHS):
        # 训练阶段
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0

        train_pbar = tqdm(data_loaders['train'], desc=f"Epoch {epoch + 1}/{Config.NUM_EPOCHS} [Train]")
        for inputs, labels in train_pbar:
            inputs = inputs.to(Config.DEVICE)
            labels = labels.to(Config.DEVICE)

            # 前向传播
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            # 反向传播和优化
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # 更新统计信息
            train_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs, 1)
            train_correct += (predicted == labels).sum().item()
            train_total += labels.size(0)

            # 更新进度条
            train_pbar.set_postfix({'loss': loss.item(), 'acc': train_correct / train_total})

        # 计算训练集平均损失和准确率
        train_loss = train_loss / len(data_loaders['train'].dataset)
        train_acc = train_correct / train_total

        # 验证阶段
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0

        val_pbar = tqdm(data_loaders['val'], desc=f"Epoch {epoch + 1}/{Config.NUM_EPOCHS} [Val]")
        with torch.no_grad():
            for inputs, labels in val_pbar:
                inputs = inputs.to(Config.DEVICE)
                labels = labels.to(Config.DEVICE)

                # 前向传播
                outputs = model(inputs)
                loss = criterion(outputs, labels)

                # 更新统计信息
                val_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs, 1)
                val_correct += (predicted == labels).sum().item()
                val_total += labels.size(0)

                # 更新进度条
                val_pbar.set_postfix({'loss': loss.item(), 'acc': val_correct / val_total})

        # 计算验证集平均损失和准确率
        val_loss = val_loss / len(data_loaders['val'].dataset)
        val_acc = val_correct / val_total

        # 更新学习率
        scheduler.step(val_loss)

        # 记录训练历史
        history['train_loss'].append(train_loss)
        history['val_loss'].append(val_loss)
        history['train_acc'].append(train_acc)
        history['val_acc'].append(val_acc)

        # 输出训练信息
        logger.info(f"Epoch {epoch + 1}/{Config.NUM_EPOCHS}")
        logger.info(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")
        logger.info(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")

        # 早停检查
        early_stopping(val_loss, model)
        if early_stopping.early_stop:
            logger.info("Early stopping triggered")
            break

    # 训练结束时间
    end_time = time.time()
    logger.info(f"Training completed in {(end_time - start_time) / 60:.2f} minutes")

    # 绘制训练历史
    plot_training_history(history, os.path.join(Config.RESULT_DIR, 'training_history.png'))

    # 加载最佳模型
    model.load_state_dict(torch.load(model_save_path))

    # 在测试集上评估模型
    logger.info("Evaluating model on test set...")
    model.eval()
    test_loss = 0.0
    all_labels = []
    all_predictions = []
    all_probabilities = []

    with torch.no_grad():
        for inputs, labels in tqdm(data_loaders['test'], desc="Testing"):
            inputs = inputs.to(Config.DEVICE)
            labels = labels.to(Config.DEVICE)

            # 前向传播
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            # 更新统计信息
            test_loss += loss.item() * inputs.size(0)

            # 获取预测结果
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            _, predicted = torch.max(outputs, 1)

            all_labels.extend(labels.cpu().numpy())
            all_predictions.extend(predicted.cpu().numpy())
            all_probabilities.extend(probabilities.cpu().numpy())

    # 计算测试集平均损失
    test_loss = test_loss / len(data_loaders['test'].dataset)
    logger.info(f"Test Loss: {test_loss:.4f}")

    # 计算评估指标
    metrics = calculate_metrics(all_labels, all_predictions, np.array(all_probabilities))
    for metric_name, metric_value in metrics.items():
        logger.info(f"{metric_name}: {metric_value:.4f}")

    # 绘制混淆矩阵
    plot_confusion_matrix(
        all_labels, all_predictions,
        os.path.join(Config.RESULT_DIR, 'confusion_matrix.png')
    )

    # 保存分类报告
    save_classification_report(
        all_labels, all_predictions,
        os.path.join(Config.RESULT_DIR, 'classification_report.csv')
    )

    # 保存最终模型
    final_model_path = os.path.join(Config.MODEL_SAVE_DIR, 'final_model.pth')
    torch.save({
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'history': history,
        'config': {k: v for k, v in Config.__dict__.items() if not k.startswith('__')}
    }, final_model_path)
    logger.info(f"Final model saved to {final_model_path}")

    return model, history, metrics


if __name__ == "__main__":
    train()
