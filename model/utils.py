import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import os
import cv2
from config import Config


class EarlyStopping:
    """早停模块，用于防止过拟合"""

    def __init__(self, patience=5, verbose=False, delta=0, path='checkpoint.pt'):
        """
        初始化早停

        Args:
            patience: 容忍多少个epoch没有提升
            verbose: 是否打印信息
            delta: 最小改善量
            path: 模型保存路径
        """
        self.patience = patience
        self.verbose = verbose
        self.delta = delta
        self.path = path
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf

    def __call__(self, val_loss, model):
        """
        调用早停

        Args:
            val_loss: 验证集损失
            model: 模型
        """
        score = -val_loss

        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
        elif score < self.best_score + self.delta:
            self.counter += 1
            if self.verbose:
                print(f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
            self.counter = 0

    def save_checkpoint(self, val_loss, model):
        """
        保存模型

        Args:
            val_loss: 验证集损失
            model: 模型
        """
        if self.verbose:
            print(f'Validation loss decreased ({self.val_loss_min:.6f} --> {val_loss:.6f}). Saving model ...')
        torch.save(model.state_dict(), self.path)
        self.val_loss_min = val_loss


def plot_confusion_matrix(y_true, y_pred, save_path):
    """
    绘制混淆矩阵

    Args:
        y_true: 真实标签
        y_pred: 预测标签
        save_path: 保存路径
    """
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=[Config.BEHAVIOR_CLASSES[i] for i in range(Config.NUM_CLASSES)],
                yticklabels=[Config.BEHAVIOR_CLASSES[i] for i in range(Config.NUM_CLASSES)])
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def save_classification_report(y_true, y_pred, save_path):
    """
    保存分类报告

    Args:
        y_true: 真实标签
        y_pred: 预测标签
        save_path: 保存路径
    """
    report = classification_report(
        y_true, y_pred,
        target_names=[Config.BEHAVIOR_CLASSES[i] for i in range(Config.NUM_CLASSES)],
        output_dict=True
    )

    # 保存为CSV文件
    import pandas as pd
    df = pd.DataFrame(report).transpose()
    df.to_csv(save_path)

    # 返回报告字典
    return report


def plot_training_history(history, save_path):
    """
    绘制训练历史

    Args:
        history: 训练历史字典
        save_path: 保存路径
    """
    plt.figure(figsize=(12, 4))

    # 损失曲线
    plt.subplot(1, 2, 1)
    plt.plot(history['train_loss'], label='Train Loss')
    plt.plot(history['val_loss'], label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.title('Training and Validation Loss')

    # 准确率曲线
    plt.subplot(1, 2, 2)
    plt.plot(history['train_acc'], label='Train Accuracy')
    plt.plot(history['val_acc'], label='Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.title('Training and Validation Accuracy')

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def draw_detection_results(frame, predictions, confidence_threshold=0.5):
    """
    在视频帧上绘制检测结果

    Args:
        frame: 输入帧
        predictions: 预测结果
        confidence_threshold: 置信度阈值

    Returns:
        frame: 带有检测结果的帧
    """
    h, w = frame.shape[:2]

    # 绘制类别预测
    class_id = predictions['class_id']
    class_name = Config.BEHAVIOR_CLASSES[class_id]
    confidence = predictions['confidence']

    # 在右上角绘制预测结果
    cv2.putText(frame, f"Behavior: {class_name}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, f"Confidence: {confidence:.2f}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # 显示警告
    if class_id != 0 and confidence > confidence_threshold:  # 不是正常行为且置信度高
        cv2.putText(frame, "WARNING!", (w - 150, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        # 闪烁效果
        if (cv2.getTickCount() // 15) % 2:  # 每15个时钟周期闪烁一次
            cv2.rectangle(frame, (0, 0), (w, h), (0, 0, 255), 10)

    return frame


def calculate_metrics(y_true, y_pred, probabilities=None):
    """
    计算各种评估指标

    Args:
        y_true: 真实标签
        y_pred: 预测标签
        probabilities: 预测概率 (可选)

    Returns:
        metrics: 指标字典
    """
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision_macro': precision_score(y_true, y_pred, average='macro'),
        'recall_macro': recall_score(y_true, y_pred, average='macro'),
        'f1_macro': f1_score(y_true, y_pred, average='macro'),
        'precision_weighted': precision_score(y_true, y_pred, average='weighted'),
        'recall_weighted': recall_score(y_true, y_pred, average='weighted'),
        'f1_weighted': f1_score(y_true, y_pred, average='weighted')
    }

    # 如果提供了概率，计算ROC-AUC
    if probabilities is not None:
        if Config.NUM_CLASSES == 2:
            metrics['roc_auc'] = roc_auc_score(y_true, probabilities[:, 1])
        else:
            metrics['roc_auc'] = roc_auc_score(y_true, probabilities, multi_class='ovr', average='macro')

    return metrics
