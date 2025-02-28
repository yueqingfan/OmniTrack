<template>
  <div class="container">
    <!-- 首页仪表盘 -->
    <div class="dashboard">
      <div class="video-container">
        <h2>实时视频监控</h2>
        <!-- 视频播放元素，绑定动态视频源 -->
        <video class="video" ref="video" controls autoplay></video>
      </div>
      <!-- 异常行为与预警展示 -->
      <div class="alerts">
        <h3>实时预警</h3>
        <div v-if="alertMessage" class="alert-card warning">
          <h4>{{ alertMessage }}</h4>
          <p>{{ alertDescription }}</p>
        </div>
        <div v-if="detectionMessage" class="alert-card success">
          <h4>{{ detectionMessage }}</h4>
          <p>{{ detectionDescription }}</p>
        </div>
      </div>
    </div>

    <!-- 控制面板 -->
    <div class="controls">
      <button @click="togglePause" class="control-btn">暂停/播放</button>
      <button @click="captureImage" class="control-btn">截图</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      alertMessage: "警报：异常聚集检测到！",
      alertDescription: "检测到某区域内人员迅速聚集，请注意调查。",
      detectionMessage: "行为识别：闯入检测",
      detectionDescription: "检测到有人员闯入禁区，请立即响应。",
    };
  },
  mounted() {
    // 调用方法来打开摄像头并显示视频流
    this.startCamera();
  },
  methods: {
    // 播放/暂停控制
    togglePause() {
      const video = this.$refs.video;
      if (video.paused) {
        video.play();
      } else {
        video.pause();
      }
    },
    // 截图功能
    captureImage() {
      const video = this.$refs.video;
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      const dataUrl = canvas.toDataURL('image/png');
      console.log('截图保存：', dataUrl);
    },
    // 打开摄像头并显示视频流
    async startCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,  // 请求视频流
        });
        const video = this.$refs.video;
        video.srcObject = stream;  // 将流绑定到video元素
      } catch (err) {
        console.error("摄像头访问失败:", err);
      }
    },
  },
};
</script>

<style scoped>
/* Global Styles */
body {
  font-family: 'Arial', sans-serif;
  background-color: #f4f6f9;
  margin: 0;
  padding: 0;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.dashboard {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
  margin-bottom: 20px;
}

.video-container {
  width: 60%;
  background-color: #000;
  border-radius: 10px;
  overflow: hidden;
}

video {
  width: 100%;
  height: auto;
}

.alerts {
  width: 35%;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.alert-card {
  padding: 15px;
  margin: 10px 0;
  border-radius: 5px;
}

.warning {
  background-color: #ffcccc;
  border-left: 5px solid #ff0000;
}

.success {
  background-color: #ccffcc;
  border-left: 5px solid #00cc00;
}

.controls {
  margin-top: 20px;
}

.control-btn {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  margin: 0 10px;
}

.control-btn:hover {
  background-color: #0056b3;
}

h2, h3 {
  font-size: 24px;
  color: #333;
}

h4 {
  font-size: 18px;
  margin-bottom: 5px;
  color: #555;
}

p {
  font-size: 14px;
  color: #777;
}
</style>
