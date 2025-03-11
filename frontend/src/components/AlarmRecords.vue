<template>
  <div class="alarm-records">
    <h1>报警记录</h1>
    <ul v-if="logs.length > 0">
      <li v-for="(record, index) in logs" :key="index" class="record-item">
        <p><strong>时间:</strong> {{ record.timestamp }}</p>
        <p><strong>检测结果:</strong> {{ record.label }} (置信度: {{ record.confidence }})</p>
        <!-- 直接使用 record.image_url -->
        <img :src="record.image_url" alt="报警截图" v-if="record.image_url" />
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
        this.logs = response.data;
      } catch (error) {
        console.error("获取报警记录失败:", error);
      }
    }
  }
};
</script>

<style scoped>
.alarm-records {
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}
.alarm-records ul {
  list-style: none;
  padding: 0;
}
.record-item {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
}
.record-item img {
  max-width: 100%;
  height: auto;
  margin-top: 10px;
  border: 1px solid #ccc;
}
.btn {
  display: inline-block;
  margin-top: 20px;
  padding: 8px 16px;
  background: #4CAF50;
  color: #fff;
  text-decoration: none;
  border-radius: 4px;
}
</style>
