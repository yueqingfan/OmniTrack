<template>
  <div class="container">
    <header class="header">
      <h1>Omnitrack 危险行为实时监控系统</h1>
      <div class="nav-bar">
        <router-link to="/alarmrecords" class="nav-btn">报警日志</router-link>
      </div>
    </header>

    <div class="main-content">
      <aside class="sidebar">
        <div class="video-settings-panel">
          <div class="video-source">
            <label>
              <input type="radio" value="camera" v-model="videoSource" />
              📹 实时摄像头
            </label>
            <label>
              <input type="radio" value="local" v-model="videoSource" />
              🎞️ 本地视频
            </label>
          </div>
          <div class="upload-section" v-if="videoSource === 'local'">
            <div class="file-input-container">
              <label class="file-input-label">
                📁选择视频
                <input type="file" accept="video/*" @change="handleVideoUpload" class="file-input" />
              </label>
            </div>
            <span class="file-name" v-if="currentFileName">📄 {{ currentFileName }}</span>
          </div>
        </div>

        <div class="settings-panel">
          <h2>系统设置 ⚙️</h2>
          <div class="settings">
            <div class="settings-group">
              <label>
                🔧 警报灵敏度:
                <div class="range-container">
                  <input type="range" min="1" max="10" v-model="alertThreshold" />
                  <span class="threshold-display">{{ alertThreshold }}</span>
                </div>
              </label>
              <div class="helper-text">值越低，系统越敏感，检测到异常行为的概率越高</div>
            </div>
            <div class="settings-group">
              <label>
                ⏳ 检测频率:
                <div class="range-container">
                  <input type="range" min="1" max="10" v-model="detectionFrequency" />
                  <span class="threshold-display">{{ detectionFrequency }}</span>
                </div>
              </label>
              <div class="helper-text">值越高，每秒分析的帧数越多，但可能增加系统负载</div>
            </div>
          </div>
        </div>
      </aside>
      <div class="main-display">
        <audio ref="alarmSound" src="alarm.mp3" preload="auto"></audio>
        <div class="alarm-banner" v-if="alarmOn">
          <div class="alarm-icon">⚠️</div>
          <div class="alarm-content">
            <h2>警报：检测到异常行为！</h2>
            <p v-if="currentAlarm" class="detection-result">
              检测结果：<strong>{{ currentAlarm.label }}</strong>
              ({{ (currentAlarm.confidence * 100).toFixed(1) }}%)
            </p>
          </div>
          <button class="stop-alarm-btn" @click="stopAlarm">🛑 停止警报</button>
        </div>
        <div class="video-container">
          <video ref="video" class="video-stream" width="640" height="480" autoplay></video>
          <div class="controls" v-if="videoSource === 'camera'">
            <button class="btn toggle-btn" @click="toggleCamera">
              {{ isCameraOn ? '📴 关闭摄像头' : '📹 开启摄像头' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <footer class="footer">
      <p>&copy; 2025 Omnitrack 危险行为智能识别系统 🚨</p>
    </footer>
  </div>
</template>
<style scoped>
:root {
  --primary-color: #e0e0e0;
  --secondary-color: #f5f5f5;
  --accent-color: #4a90e2;
  --accent-hover: #6bb8ff;
  --danger-color: #ff4d4d;
  --success-color: #4caf50;
  --success-hover: #66bb6a;
  --text-light: #ffffff;
  --border-radius: 12px;
  --box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

html, body {
  margin: 0;
  padding: 0;
  min-height: 100%;
  background: #fff;
}
.container {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: #333;
  padding: 30px;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  max-width: 1000px;
  margin: 40px auto;
}

.header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #333; /* 标题使用深色文字 */
  background: none; /* 去除文字渐变 */
  -webkit-background-clip: unset;
  -webkit-text-fill-color: unset;
  letter-spacing: -0.5px;
}

.nav-bar {
  display: flex;
  gap: 15px;
  font-size: 24px;
}

.nav-btn {
  background-color: var(--accent-color);
  padding: 12px 24px;
  border-radius: 30px;
  color: var(--text-light);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.nav-btn::before {
  content: "📋";
  font-size: 24px;
}

.nav-btn:hover {
  background-color: var(--accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.main-content {
  display: flex;
  gap: 20px;
}
.sidebar {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background-color: rgba(0, 0, 0, 0.03);
  padding: 20px;
  border-radius: var(--border-radius);
}

.video-settings-panel,
.settings-panel {
  background-color: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: var(--border-radius);
  margin-bottom: 10px;
}

.video-settings-panel .video-source {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.video-settings-panel .video-source label {
  font-size: 1.1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.upload-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.file-input-container {
  position: relative;
  overflow: hidden;
}

.file-input-label {
  display: inline-block;
  background-color: var(--accent-color);
  color: var(--text-light);
  padding: 12px 24px;
  border-radius: 30px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;

  margin-left: -20px;
}


.file-input-label:hover {
  background-color: var(--accent-hover);
  transform: translateY(-2px);
}

.file-input-label::before {
  margin-right: 0px;
}

.file-input {
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.file-name {
  font-size: 0.9rem;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-right:5px;
}

.settings-panel h2 {
  font-size: 1.8rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: -20px;

}

.settings {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.settings-group label {
  font-size: 1.1rem;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.range-container {
  display: flex;
  align-items: center;
  gap: 15px;
}

input[type=\"range\"] {
  width: 100%;
  accent-color: var(--accent-color);
  height: 8px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.2);
}

.threshold-display {
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
  border-radius: 50%;
  font-weight: bold;
}

.helper-text {
  font-size: 0.9rem;
  color: rgba(0, 0, 0, 0.7);
}

.main-display {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.alarm-banner {
  display: flex;
  align-items: center;
  gap: 20px;
  background-color: var(--danger-color);
  color: #ff4d4d; /* 保证文字在红色背景上可见 */
  padding: 20px;
  border-radius: var(--border-radius);
  box-shadow: 0 0 20px rgba(255, 77, 77, 0.5);
  animation: pulse 1.5s infinite alternate; /* 轻微的呼吸动画 */
  margin-bottom: 20px; /* 与下方内容留出距离 */
}

@keyframes pulse {
  0% {
    opacity: 0.9;
    transform: scale(0.98);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* 大图标区：让图标更大，并有轻微的晃动 */
.alarm-icon {
  font-size: 2.5rem;
  animation: shake 0.7s infinite alternate;
}

@keyframes shake {
  0% { transform: translateX(-3px); }
  100% { transform: translateX(3px); }
}

/* 文字区：标题 + 描述 */
.alarm-content {
  flex: 1;
}

.alarm-content h2 {
  margin: 0 0 8px;
  font-size: 1.6rem;
}

.alarm-content p {
  margin: 0;
  font-size: 1.1rem;
}

/* 停止警报按钮 */
.stop-alarm-btn {
  background-color: #fff;
  color: var(--danger-color);
  border: none;
  padding: 10px 20px;
  border-radius: 30px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.stop-alarm-btn:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px);
}


.video-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}

.video-stream {
  width: 100%;
  height: auto;
  max-height: 60vh;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  background-color: #000;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.video-stream:hover {
  transform: scale(1.01);
}

.controls {
  display: flex;
  gap: 15px;
  width: 100%;
  justify-content: center;
}

.btn {
  font-size: 1rem;
  font-weight: 600;
  padding: 12px 24px;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.toggle-btn {
  background-color: var(--success-color);
  color: var(--text-light);
}

.toggle-btn:hover {
  background-color: var(--success-hover);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.footer {
  margin-top: 40px;
  text-align: center;
  font-size: 0.9rem;
  color: #333; /* 改成深色/黑色，便于在浅灰背景上查看 */
  padding-top: 20px;
  border-top: 1px solid rgba(0, 0, 0, 0.2);
}

/* 响应式布局 */
@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
  .sidebar, .main-display {
    width: 100%;
  }
  .container {
    margin: 20px;
    padding: 20px;
  }
  .header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
}
</style>


<script>
import axios from "axios";
export default {
  name: "VideoStream",
  data() {
    return {
      ws: null,
      videoStream: null,
      isCameraOn: false,
      frameSending: false,
      frameCounter: 0,
      requestFrameId: null,
      serverMessage: null,
      videoSource: "camera",
      localVideoActive: false,
      currentFileName: "",
      previewImage: "",
      alarmOn: false,
      logs: [],
      alertThreshold: 5,
      detectionFrequency: 5,
      lastFrameTime: 0,
      previousLabel: null,
      sessionId: this.generateUniqueId(),
      currentAlarm: null,
      alarmCooldown: false,
      alarmCooldownTime: 5000,
      alarmQueue: [],
      lastAlarmTime: 0,
      componentKey: 0
    };
  },
  computed: {
    frameInterval() {
      return Math.round(1000 / (this.detectionFrequency * 3));
    }
  },
  methods: {
    generateUniqueId() {
      return Date.now().toString(36) + Math.random().toString(36).substr(2);
    },
    connectWebSocket() {
      if (this.ws) {
        this.ws.close();
      }
      this.ws = new WebSocket("ws://localhost:8080/video-stream");

      this.ws.onopen = () => {
        console.log("Connected to WebSocket server");
      };

      this.ws.onmessage = (event) => {
        console.log("Received message from server:", event.data);
        const prefix = "CLIP Analysis:";
        let dataStr = event.data;
        if (dataStr.startsWith(prefix)) {
          dataStr = dataStr.slice(prefix.length).trim();
        }
        try {
          const dataObj = JSON.parse(dataStr);

          // 将置信度保留两位小数
          let confidence = parseFloat(dataObj.confidence);
          confidence = Number(confidence.toFixed(2));

          // 转换标签为小写方便匹配
          const labelText = dataObj.label.toLowerCase();
          let category = "normal";
          if (labelText.includes("abuse") ||
              labelText.includes("domestic violence") ||
              labelText.includes("child abuse") ||
              labelText.includes("elder abuse")) {
            category = "虐待";
          } else if (labelText.includes("shoot") ||
              labelText.includes("shooting") ||
              labelText.includes("gun") ||
              labelText.includes("firearm") ||
              labelText.includes("sniper") ||
              labelText.includes("firefight") ||
              labelText.includes("robbery")) {
            category = "枪击";
          } else if (labelText.includes("fight") ||
              labelText.includes("brawl") ||
              labelText.includes("altercation")) {
            category = "打架";
          } else if (labelText.includes("theft") ||
              labelText.includes("robbery") ||
              labelText.includes("burglary") ||
              labelText.includes("shoplifting") ||
              labelText.includes("pickpocket") ||
              labelText.includes("snatching") ||
              labelText.includes("hijacking") ||
              labelText.includes("stealing") ||
              labelText.includes("smash-and-grab") ||
              labelText.includes("package theft") ||
              labelText.includes("car theft") ||
              labelText.includes("motorcycle theft") ||
              labelText.includes("bicycle theft")
          ) {
            category = "盗窃";
          } else if (labelText.includes("explosion") ||
              labelText.includes("bomb") ||
              labelText.includes("blast") ||
              labelText.includes("detonation") ||
              labelText.includes("fireball")) {
            category = "爆炸";
          } else if ((labelText.includes("fire") &&
                  !labelText.includes("gunfire") &&
                  !labelText.includes("firefight")) ||
              labelText.includes("burn") ||
              labelText.includes("flame") ||
              labelText.includes("smoke")) {
            category = "火灾";
          }

          this.serverMessage = {
            label: category,
            confidence: confidence
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
        setTimeout(() => {
          this.connectWebSocket();
        }, 3000);
      };
    },
    async startCamera() {
      try {
        // 重置警报状态
        this.resetAlarmState();

        this.videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
        this.$refs.video.srcObject = this.videoStream;
        this.isCameraOn = true;
        this.localVideoActive = false;
        this.startSendingFrames();
      } catch (err) {
        console.error("Error accessing camera: " + err);
        this.showNotification("摄像头访问失败，请检查设备权限", "error");
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

    handleVideoUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // 重置状态
        this.resetAlarmState();

        // 停止当前摄像头或本地视频
        if (this.isCameraOn) {
          this.stopCamera();
        }

        const url = URL.createObjectURL(file);
        this.$refs.video.srcObject = null;
        this.$refs.video.src = url;
        this.localVideoActive = true;
        this.currentFileName = file.name;
        this.videoSource = `local:${file.name}`;

        console.log("切换新视频:", file.name);

        this.$refs.video.addEventListener("loadeddata", () => {
          this.startSendingFrames();
        });
      }
    },
    resetAlarmState() {
      this.alarmOn = false;
      this.previousLabel = null;
      this.currentAlarm = null;
      this.serverMessage = null;
      this.previewImage = "";
      this.alarmQueue = [];
      this.lastAlarmTime = 0;

      if (this.$refs.alarmSound) {
        this.$refs.alarmSound.pause();
        this.$refs.alarmSound.currentTime = 0;
      }
    },

    // 将当前视频帧转换为 Blob 并发送给服务器
    sendVideoFrame() {
      const now = Date.now();

      // 根据检测频率控制帧发送
      if (now - this.lastFrameTime < this.frameInterval) {
        // 如果时间间隔小于设定值，则跳过此帧
        this.requestFrameId = requestAnimationFrame(this.sendVideoFrame);
        return;
      }

      this.lastFrameTime = now;

      if ((this.videoSource === "camera" && !this.isCameraOn) ||
          (this.videoSource === "local" && !this.localVideoActive) ||
          !this.ws || this.ws.readyState !== WebSocket.OPEN) {
        this.requestFrameId = requestAnimationFrame(this.sendVideoFrame);
        return;
      }

      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      const video = this.$refs.video;

      // 确保视频已经加载
      if (!video || !video.videoWidth || !video.videoHeight) {
        this.requestFrameId = requestAnimationFrame(this.sendVideoFrame);
        return;
      }

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      // 生成预览图（调试用）
      const dataUrl = canvas.toDataURL("image/jpeg", 0.9);
      this.previewImage = dataUrl;

      // 将帧转换为 Blob 并发送给服务器
      canvas.toBlob((blob) => {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          this.ws.send(blob);
        }
        this.requestFrameId = requestAnimationFrame(this.sendVideoFrame);
      }, "image/jpeg", 0.9);
    },

    // 开始循环发送视频帧
    startSendingFrames() {
      if (this.frameSending) return;
      this.frameSending = true;
      this.lastFrameTime = 0; // 重置时间戳
      this.sendVideoFrame();
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
      const now = Date.now();
      if (this.alarmCooldown) {
        const existingAlarm = this.alarmQueue.find(alarm => alarm.label === this.serverMessage.label);
        if (!existingAlarm) {
          // 将新的警报添加到队列
          this.alarmQueue.push({
            label: this.serverMessage.label,
            confidence: this.serverMessage.confidence,
            timestamp: now
          });
          console.log("警报冷却中，添加到队列:", this.serverMessage.label);
        }
        return;
      }
      if (this.previousLabel === this.serverMessage.label &&
          (now - this.lastAlarmTime < this.alarmCooldownTime)) {
        return;
      }
      this.alarmOn = true;
      this.currentAlarm = {
        label: this.serverMessage.label,
        confidence: this.serverMessage.confidence
      };
      this.lastAlarmTime = now;
      if (this.$refs.alarmSound) {
        this.$refs.alarmSound.play().catch(e => console.error("无法播放警报声:", e));
      }
      const screenshot = this.captureScreenshot();
      try {
        const response = await axios.post("http://localhost:8080/api/alarms", {
          label: this.serverMessage.label,
          confidence: this.serverMessage.confidence,
          imageUrl: screenshot
        });
        console.log("报警数据存入数据库:", response.data);
        this.previousLabel = this.serverMessage.label;
        this.alarmCooldown = true;
        setTimeout(() => {
          this.processAlarmQueue();
        }, this.alarmCooldownTime);

      } catch (error) {
        console.error("报警数据存入数据库失败:", error);
        this.alarmCooldown = false; // 发生错误时重置冷却状态
      }
    },
    processAlarmQueue() {
      this.alarmCooldown = false;

      // 如果队列中有警报，处理最近的一个
      if (this.alarmQueue.length > 0) {
        // 按时间戳排序，获取最近的警报
        this.alarmQueue.sort((a, b) => b.timestamp - a.timestamp);
        const nextAlarm = this.alarmQueue.shift();
        this.serverMessage = {
          label: nextAlarm.label,
          confidence: nextAlarm.confidence
        };
        this.alarmQueue = this.alarmQueue.filter(alarm => alarm.label !== nextAlarm.label);
        this.triggerAlarm();
      }
    },
    stopAlarm() {
      this.alarmOn = false;
      if (this.$refs.alarmSound) {
        this.$refs.alarmSound.pause();
        this.$refs.alarmSound.currentTime = 0;
      }
      this.alarmCooldown = false;
      if (this.alarmQueue.length > 0) {
        this.$nextTick(() => {
          this.processAlarmQueue();
        });
      }
    },
    showNotification(message, type = 'info') {
      console.log(`[${type}]`, message);
    }
  },
  watch: {
    // 保留现有的serverMessage监视器
    serverMessage(newVal) {
      if (newVal && newVal.label) {
        const threshold = this.alertThreshold / 10;
        if (newVal.label !== "normal" && newVal.confidence >= threshold) {
          this.triggerAlarm();
        } else {
          this.alarmOn = false;
        }
      }
    },

    watch: {
      videoSource() {
        this.stopSendingFrames();
        this.ws.send("RESET");
        this.ws.onmessage = (event) => {
          if (event.data === "RESET_OK") {
            this.startSendingFrames();
          }
        };
      }
    }
  },
  mounted() {
    const alarmSound = this.$refs.alarmSound;
    alarmSound.load();
    alarmSound.play().then(() => {
      alarmSound.pause();
    }).catch((error) => {
      console.error("音频预加载失败:", error);
    });
    this.connectWebSocket();
    const storedLogs = localStorage.getItem("alarmLogs");
    if (storedLogs) {
      this.logs = JSON.parse(storedLogs);
    }
    const video = this.$refs.video;
    if (video) {
      video.addEventListener('ended', this.resetAlarmState);
      video.addEventListener('error', this.resetAlarmState);
      video.addEventListener('pause', this.resetAlarmState);
    }
  },
  beforeUnmount() {
    if (this.ws) {
      this.ws.close();
    }
    this.stopCamera();

    const video = this.$refs.video;
    if (video) {
      video.removeEventListener('ended', this.resetAlarmState);
      video.removeEventListener('error', this.resetAlarmState);
      video.removeEventListener('pause', this.resetAlarmState);
    }
  }
};
</script>