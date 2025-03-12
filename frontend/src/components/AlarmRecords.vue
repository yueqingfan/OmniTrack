<template>
  <div class="alarm-records">
    <h1>报警记录</h1>
    <ul v-if="logs.length > 0">
      <li v-for="(record, index) in logs" :key="index" class="record-item">
        <p><strong>时间:</strong> {{ record.timestamp }}</p>
        <p><strong>检测结果:</strong> {{ record.label }} (置信度: {{ record.confidence }})</p>
        <div class="image-container" v-if="record.imageUrl">
          <img :src="record.imageUrl" alt="报警截图" @error="(e) => handleImageError(e, record)" />
        </div>
      </li>
    </ul>
    <p v-else>暂无报警记录</p>
    <router-link to="/dashboard" class="btn">返回监控页面</router-link>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "AlarmRecords",
  data() {
    return {
      logs: []
    };
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
        console.log('获取到的第一条记录:', this.logs[0]);
      } catch (error) {
        console.error("获取报警记录失败:", error);
      }
    },
    handleImageError(e, record) {
      console.error('图片加载失败:', {
        url: record.imageUrl,
        error: e
      });
    }
  }
};
</script>

<style scoped>
.alarm-records {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.record-item {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.image-container {
  margin-top: 10px;
}

.image-container img {
  max-width: 100%;
  max-height: 300px;
  border: 1px solid #ddd;
}

.btn {
  display: inline-block;
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}
</style>