import torch
import torch.nn as nn
import torch.nn.functional as F
from config import Config


class YOLOLSTM(nn.Module):
    """
    YOLOv8 + LSTM 模型
    """

    def __init__(self, input_size=Config.YOLO_FEATURE_SIZE, hidden_size=Config.LSTM_HIDDEN_SIZE,
                 num_layers=Config.LSTM_NUM_LAYERS, num_classes=Config.NUM_CLASSES):
        """
        初始化模型

        Args:
            input_size: 输入特征大小
            hidden_size: LSTM隐藏层大小
            num_layers: LSTM层数
            num_classes: 行为类别数
        """
        super(YOLOLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # LSTM层
        self.lstm = nn.LSTM(
            input_size,
            hidden_size,
            num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=Config.DROPOUT_RATE if num_layers > 1 else 0
        )

        # 注意力机制
        self.attention = nn.Sequential(
            nn.Linear(hidden_size * 2, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, 1),
            nn.Softmax(dim=1)
        )

        # 全连接层
        self.fc = nn.Sequential(
            nn.Linear(hidden_size * 2, hidden_size),
            nn.BatchNorm1d(hidden_size),
            nn.ReLU(),
            nn.Dropout(Config.DROPOUT_RATE),
            nn.Linear(hidden_size, num_classes)
        )

    def forward(self, x):
        """
        前向传播

        Args:
            x: 输入特征 [batch_size, seq_len, input_size]

        Returns:
            outputs: 分类结果 [batch_size, num_classes]
        """
        # 初始化隐藏状态和单元状态
        h0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).to(x.device)

        # LSTM前向传播
        lstm_out, _ = self.lstm(x, (h0, c0))  # [batch_size, seq_len, hidden_size*2]

        # 应用注意力机制
        attention_weights = self.attention(lstm_out)  # [batch_size, seq_len, 1]
        context = torch.sum(attention_weights * lstm_out, dim=1)  # [batch_size, hidden_size*2]

        # 全连接层
        outputs = self.fc(context)

        return outputs


class YOLOLSTMv2(nn.Module):
    """
    YOLOv8 + LSTM 模型 (改进版)
    """

    def __init__(self, input_size=Config.YOLO_FEATURE_SIZE, hidden_size=Config.LSTM_HIDDEN_SIZE,
                 num_layers=Config.LSTM_NUM_LAYERS, num_classes=Config.NUM_CLASSES):
        """
        初始化模型

        Args:
            input_size: 输入特征大小
            hidden_size: LSTM隐藏层大小
            num_layers: LSTM层数
            num_classes: 行为类别数
        """
        super(YOLOLSTMv2, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # 特征压缩层
        self.feature_encoder = nn.Sequential(
            nn.Linear(input_size, input_size // 2),
            nn.ReLU(),
            nn.BatchNorm1d(Config.SAMPLE_FRAMES),
            nn.Linear(input_size // 2, input_size // 2),
            nn.ReLU(),
            nn.BatchNorm1d(Config.SAMPLE_FRAMES)
        )

        # LSTM层
        self.lstm = nn.LSTM(
            input_size // 2,
            hidden_size,
            num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=Config.DROPOUT_RATE if num_layers > 1 else 0
        )

        # 时间卷积
        self.tcn = nn.Sequential(
            nn.Conv1d(hidden_size * 2, hidden_size, kernel_size=3, padding=1),
            nn.BatchNorm1d(hidden_size),
            nn.ReLU(),
            nn.Conv1d(hidden_size, hidden_size, kernel_size=3, padding=1),
            nn.BatchNorm1d(hidden_size),
            nn.ReLU()
        )

        # 全局平均池化
        self.global_avg_pool = nn.AdaptiveAvgPool1d(1)

        # 全连接层
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.BatchNorm1d(hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(Config.DROPOUT_RATE),
            nn.Linear(hidden_size // 2, num_classes)
        )

    def forward(self, x):
        """
        前向传播

        Args:
            x: 输入特征 [batch_size, seq_len, input_size]

        Returns:
            outputs: 分类结果 [batch_size, num_classes]
        """
        batch_size, seq_len, _ = x.shape

        # 特征压缩
        x = self.feature_encoder(x)  # [batch_size, seq_len, input_size//2]

        # 初始化隐藏状态和单元状态
        h0 = torch.zeros(self.num_layers * 2, batch_size, self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers * 2, batch_size, self.hidden_size).to(x.device)

        # LSTM前向传播
        lstm_out, _ = self.lstm(x, (h0, c0))  # [batch_size, seq_len, hidden_size*2]

        # 变换形状用于时间卷积
        tcn_input = lstm_out.permute(0, 2, 1)  # [batch_size, hidden_size*2, seq_len]
        tcn_out = self.tcn(tcn_input)  # [batch_size, hidden_size, seq_len]

        # 全局平均池化
        pooled = self.global_avg_pool(tcn_out).squeeze(-1)  # [batch_size, hidden_size]

        # 全连接层
        outputs = self.fc(pooled)

        return outputs