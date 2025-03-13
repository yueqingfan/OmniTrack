<template>
  <div class="alarm-records">
    <h1>报警记录</h1>
    <div class="layout-container">
      <div class="left-column">
        <button class="btn btn-info" @click="generateReport">生成分析报告</button>
        <div v-if="analysisReport" class="report-container">
          <h2>报警分析报告</h2>
          <p><strong>报警总数：</strong> {{ analysisReport.totalAlarms }}</p>
          <p><strong>平均置信度：</strong> {{ analysisReport.averageConfidence }}</p>
          <p><strong>报警类型分布：</strong></p>
          <ul>
            <li v-for="(count, label) in analysisReport.alarmsByLabel" :key="label">
              {{ label }}: {{ count }} 次
            </li>
          </ul>
          <p><strong>时间范围：</strong> {{ analysisReport.endTime }} - {{ analysisReport.startTime }}</p>
        </div>
      </div>
      <div class="center-column">
        <div class="filter-container">
          <label for="filter">按异常类型筛选:</label>
          <select id="filter" v-model="selectedLabel">
            <option value="">全部</option>
            <option v-for="(label, index) in uniqueLabels" :key="index" :value="label">
              {{ label }}
            </option>
          </select>
        </div>
        <ul v-if="filteredLogs.length > 0">
          <li v-for="(record, index) in filteredLogs" :key="index" class="record-item">
            <p><strong>时间:</strong> {{ record.timestamp }}</p>
            <p>
              <strong>检测结果:</strong> {{ record.label }}
              (置信度: {{ (record.confidence * 100).toFixed(1) }}%)
            </p>
            <div class="image-container" v-if="record.imageUrl">
              <img :src="record.imageUrl" alt="报警截图" @error="(e) => handleImageError(e, record)" />
            </div>
          </li>
        </ul>
        <p v-else>暂无报警记录</p>
      </div>
      <div v-if="showImageModal" class="modal-overlay" @click="showImageModal = false">
        <img :src="modalImageUrl" class="modal-image" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "AlarmRecords",
  data() {
    return {
      logs: [],
      analysisReport: null,
      selectedLabel: "",
    };
  },
  computed: {
    uniqueLabels() {
      const labels = this.logs.map(record => record.label);
      return [...new Set(labels)];
    },
    filteredLogs() {
      if (!this.selectedLabel) {
        return this.logs;
      }
      return this.logs.filter(record => record.label === this.selectedLabel);
    },
  },
  mounted() {
    this.fetchAlarmRecords();
  },
  methods: {
    async fetchAlarmRecords() {
      try {
        const response = await axios.get("http://localhost:8080/api/alarms");
        this.logs = response.data.map(record => {
          return {
            ...record,
            imageUrl: record.imageUrl ? record.imageUrl.trim() : ''
          };
        });
      } catch (error) {
        console.error("获取报警记录失败:", error);
      }
    },
    handleImageError(e, record) {
      console.error('图片加载失败:', { url: record.imageUrl, error: e });
    },
    generateReport() {
      if (this.logs.length === 0) {
        alert("暂无报警记录生成报告");
        return;
      }
      let totalAlarms = this.logs.length;
      let sumConfidence = 0;
      let alarmsByLabel = {};
      let startTime = this.logs[0].timestamp;
      let endTime = this.logs[this.logs.length - 1].timestamp;

      this.logs.forEach(record => {
        sumConfidence += record.confidence;
        if (alarmsByLabel[record.label]) {
          alarmsByLabel[record.label]++;
        } else {
          alarmsByLabel[record.label] = 1;
        }
      });

      let averageConfidence = (sumConfidence / totalAlarms).toFixed(2);
      this.analysisReport = {
        totalAlarms,
        averageConfidence,
        alarmsByLabel,
        startTime,
        endTime
      };
    },
  }
};
</script>

<style scoped>
.alarm-records {
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
  background: #f4f6f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.filter-container {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-container label {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.filter-container select {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
}

.layout-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.left-column, .right-column {
  width: 22%;
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.center-column {
  flex: 1;
}

.report-container {
  background: #ffffff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.record-item {
  margin-bottom: 10px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.record-item:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
}

.image-container {
  margin-top: 10px;
  display: flex;
  justify-content: center;
}

.image-container img {
  max-width: 100%;
  max-height: 400px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-image {
  max-width: 80%;
  max-height: 80%;
}
.btn {
  display: inline-block;
  padding: 10px 16px;
  font-size: 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.2s ease;
}

.btn-info {
  background-color: #007bff;
  color: white;
}

.btn-info:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}

.return-btn {
  background-color: #28a745;
  color: white;
  text-align: center;
  display: block;
  padding: 10px;
}


</style>

