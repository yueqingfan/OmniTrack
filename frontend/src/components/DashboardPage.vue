<template>
  <div class="container">
    <header class="header">
      <h1>Omnitrack 危险行为实时监控系统</h1>
      <div class="nav-bar">
        <router-link to="/alarmrecords" class="nav-btn">报警日志</router-link>
      </div>
    </header>
    <div class="video-source">
      <label>
        <input type="radio" value="camera" v-model="videoSource" /> 摄像头
      </label>
      <label>
        <input type="radio" value="local" v-model="videoSource" /> 本地视频上传
      </label>
    </div>
    <div class="upload-section" v-if="videoSource === 'local'">
      <input type="file" accept="video/*" @change="handleVideoUpload" />
    </div>
    <div class="alarm-banner" v-if="alarmOn">
      ⚠️ 警报：检测到异常行为！
      <span v-if="serverMessage">
        检测结果: {{ serverMessage.label }} ({{ serverMessage.confidence }})
      </span>
      <router-link to="/alarmrecords" class="btn">查看报警记录</router-link>
      <button class="btn stop-alarm-btn" @click="stopAlarm">停止警报</button>
    </div>
    <div class="video-container">
      <video ref="video" width="640" height="480" autoplay class="video-stream"></video>
      <div class="controls" v-if="videoSource === 'camera'">
        <button class="btn toggle-btn" @click="toggleCamera">
          {{ isCameraOn ? '关闭摄像头' : '开启摄像头' }}
        </button>
      </div>
    </div>
    <div class="additional-controls">
      <h2>系统设置</h2>
      <div class="settings">
        <label>
          警报阈值:
          <input type="range" min="1" max="10" v-model="alertThreshold" />
        </label>
        <span class="threshold-display">{{ alertThreshold }}</span>
      </div>
    </div>
    <footer class="footer">
      <p>&copy; 2025 Omnitrack 危险行为识别系统</p>
    </footer>
    <audio ref="alarmSound" src="alarm.mp3" preload="auto"></audio>
  </div>
</template>

<script>
import axios  from "axios";
export default {
  name: "VideoStream",
  data() {
    return {
      ws: null,
      videoStream: null,
      isCameraOn: false,
      frameSending: false,
      requestFrameId: null,
      // 解析后的检测结果对象：{ label, confidence }
      serverMessage: null,
      videoSource: "camera", // "camera" 或 "local"
      localVideoActive: false,
      previewImage: "",
      alarmOn: false,
      logs: [],
      alertThreshold: 5 // 警报阈值（1～10，内部转换为0～1的值）
    };
  },
  methods: {
    // 建立 WebSocket 连接
    connectWebSocket() {
      if (this.ws) {
        this.ws.close();
      }
      this.ws = new WebSocket("ws://localhost:8080/video-stream");
      this.ws.onopen = () => {
        console.log("Connected to WebSocket server");
      };
      // 接收服务器返回的消息
      this.ws.onmessage = (event) => {
        console.log("Received message from server:", event.data);
        // 消息示例：
        // "CLIP Analysis: {"label":"normal","confidence":0.9837279319763184}"
        const prefix = "CLIP Analysis:";
        let dataStr = event.data;
        if (dataStr.startsWith(prefix)) {
          dataStr = dataStr.slice(prefix.length).trim();
        }
        try {
          const dataObj = JSON.parse(dataStr);
          this.serverMessage = {
            label: dataObj.label,
            confidence: dataObj.confidence
          };
        } catch (e) {
          console.error("解析服务器消息错误:", e);
        }
      };
      this.ws.onerror = (error) => {
        console.error("WebSocket error: ", error);
      };
      this.ws.onclose = () => {
        console.log("Disconnected from WebSocket server, attempting reconnect...");
        setTimeout(this.connectWebSocket, 3000);
      };
    },

    // 打开摄像头并采集视频
    async startCamera() {
      try {
        this.videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
        this.$refs.video.srcObject = this.videoStream;
        this.isCameraOn = true;
        this.localVideoActive = false;
        this.startSendingFrames();
      } catch (err) {
        console.error("Error accessing camera: " + err);
      }
    },

    // 关闭摄像头并停止视频帧发送
    stopCamera() {
      if (this.videoStream) {
        this.videoStream.getTracks().forEach(track => track.stop());
        this.videoStream = null;
        this.isCameraOn = false;
      }
      this.stopSendingFrames();
    },

    // 切换摄像头状态（仅对摄像头模式有效）
    toggleCamera() {
      if (this.videoSource !== "camera") return;
      if (this.isCameraOn) {
        this.stopCamera();
      } else {
        this.startCamera();
      }
    },

    // 处理本地视频上传
    handleVideoUpload(event) {
      const file = event.target.files[0];
      if (file) {
        if (this.isCameraOn) {
          this.stopCamera();
        }
        const url = URL.createObjectURL(file);
        this.$refs.video.srcObject = null;
        this.$refs.video.src = url;
        this.localVideoActive = true;
        this.startSendingFrames();
      }
    },

    // 将当前视频帧转换为 Blob 并发送给服务器
    sendVideoFrame() {
      if ((this.videoSource === "camera" && !this.isCameraOn) ||
          (this.videoSource === "local" && !this.localVideoActive) ||
          !this.ws || this.ws.readyState !== WebSocket.OPEN) {
        return;
      }
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      canvas.width = this.$refs.video.videoWidth;
      canvas.height = this.$refs.video.videoHeight;
      ctx.drawImage(this.$refs.video, 0, 0, canvas.width, canvas.height);

      // 生成预览图（调试用）
      const dataUrl = canvas.toDataURL("image/jpeg", 0.9);
      this.previewImage = dataUrl;

      // 将帧转换为 Blob 并发送给服务器
      canvas.toBlob((blob) => {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          this.ws.send(blob);
        }
      }, "image/jpeg", 0.9);
    },

    // 开始循环发送视频帧
    startSendingFrames() {
      if (this.frameSending) return;
      this.frameSending = true;
      const sendFrame = () => {
        if (!this.frameSending) return;
        this.sendVideoFrame();
        this.requestFrameId = requestAnimationFrame(sendFrame);
      };
      sendFrame();
    },

    // 停止视频帧发送
    stopSendingFrames() {
      this.frameSending = false;
      if (this.requestFrameId) {
        cancelAnimationFrame(this.requestFrameId);
        this.requestFrameId = null;
      }
    },

    // 截图当前视频帧，返回 dataURL
    captureScreenshot() {
      const video = this.$refs.video;
      if (!video) return "";
      const canvas = document.createElement("canvas");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      return canvas.toDataURL("image/jpeg", 0.9);
    },

    async triggerAlarm() {
      this.alarmOn = true;
      const screenshot = this.captureScreenshot();

      try {
        const response = await axios.post("http://localhost:8080/api/alarms", {
          label: this.serverMessage.label,
          confidence: this.serverMessage.confidence,
          imageUrl: screenshot  // 直接存 Base64
        });
        console.log("报警数据存入数据库:", response.data);
      } catch (error) {
        console.error("报警数据存入数据库失败:", error);
      }
    }
    ,

    // 停止警报
    stopAlarm() {
      this.alarmOn = false;
      if (this.$refs.alarmSound) {
        this.$refs.alarmSound.pause();
        this.$refs.alarmSound.currentTime = 0;
      }
    }
  },
  watch: {
    // 当接收到检测结果时，根据 label 和 confidence 判断是否触发警报
    serverMessage(newVal) {
      if (newVal && newVal.label) {
        const threshold = this.alertThreshold / 10;
        if (newVal.label !== "normal" && newVal.confidence >= threshold) {
          this.triggerAlarm();
        } else {
          this.alarmOn = false;
        }
      }
    }
  },
  mounted() {
    this.connectWebSocket();
    // 尝试加载之前的报警日志（若存在）
    const storedLogs = localStorage.getItem("alarmLogs");
    if (storedLogs) {
      this.logs = JSON.parse(storedLogs);
    }
  },
  beforeUnmount() {
    if (this.ws) {
      this.ws.close();
    }
    this.stopCamera();
  }
};
</script>


<style scoped>
.container {
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  background: #f9f9f9;
  color: #333;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.header {
  text-align: center;
  margin-bottom: 20px;
}
.video-source {
  text-align: center;
  margin-bottom: 10px;
}
.video-source label {
  margin-right: 15px;
  font-size: 16px;
}
.upload-section {
  text-align: center;
  margin-bottom: 15px;
}
.alarm-banner {
  background-color: #ffdddd;
  color: #d8000c;
  border: 1px solid #d8000c;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
  margin-bottom: 15px;
  font-size: 18px;
}
.stop-alarm-btn {
  margin-left: 15px;
  background-color: #d8000c;
  color: #fff;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.video-container {
  text-align: center;
  margin-bottom: 20px;
}
.video-stream {
  border: 3px solid #4CAF50;
  border-radius: 4px;
}
.controls {
  margin-top: 10px;
}
.btn {
  font-size: 16px;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.toggle-btn {
  background-color: #4CAF50;
  color: #fff;
  transition: background-color 0.3s;
}
.toggle-btn:hover {
  background-color: #45a049;
}
.server-message {
  background-color: #fff3cd;
  border: 1px solid #ffeeba;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
  text-align: center;
}
.additional-controls {
  margin: 20px 0;
}
.additional-controls h2,
.additional-controls h3 {
  margin-bottom: 10px;
  text-align: center;
}
.settings {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}
.settings label {
  font-size: 16px;
  margin-right: 10px;
}
.threshold-display {
  font-weight: bold;
}
.logs ul {
  list-style: none;
  padding: 0;
  max-height: 150px;
  overflow-y: auto;
}
.logs li {
  background-color: #e9ecef;
  margin-bottom: 5px;
  padding: 8px;
  border-radius: 4px;
}
.footer {
  text-align: center;
  font-size: 14px;
  color: #777;
  margin-top: 30px;
  border-top: 1px solid #ddd;
  padding-top: 10px;
}
</style>
