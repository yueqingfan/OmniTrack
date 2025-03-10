<template>
  <div>
    <h1>实时视频</h1>
    <video ref="video" width="640" height="480" autoplay></video>
    <div>
      <button @click="toggleCamera">{{ isCameraOn ? '关闭摄像头' : '开启摄像头' }}</button>
    </div>
    <!-- 显示服务器返回的消息 -->
    <div v-if="serverMessage">
      <p>检测结果{{ serverMessage }}</p>
    </div>
  </div>
</template>


<script>
export default {
  name: "VideoStream",
  data() {
    return {
      ws: null,
      videoStream: null,
      isCameraOn: false,
      frameSending: false,
      requestFrameId: null,
      serverMessage: "",
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
        this.serverMessage = event.data;
      };

      this.ws.onerror = (error) => {
        console.error("WebSocket error: ", error);
      };

      this.ws.onclose = () => {
        console.log("Disconnected from WebSocket server, attempting reconnect...");
        setTimeout(this.connectWebSocket, 3000); // 3秒后尝试重连
      };
    },

    // 打开摄像头并开始采集视频
    async startCamera() {
      try {
        this.videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
        this.$refs.video.srcObject = this.videoStream;
        this.isCameraOn = true;
        this.startSendingFrames();
      } catch (err) {
        console.error("Error accessing camera: " + err);
      }
    },

    // 关闭摄像头并停止发送视频帧
    stopCamera() {
      if (this.videoStream) {
        this.videoStream.getTracks().forEach(track => track.stop());
        this.videoStream = null;
        this.isCameraOn = false;
      }
      this.stopSendingFrames();
    },

    // 切换摄像头状态
    toggleCamera() {
      if (this.isCameraOn) {
        this.stopCamera();
      } else {
        this.startCamera();
      }
    },

    // 将当前视频帧转换为 Blob 并发送给服务器
    sendVideoFrame() {
      if (!this.isCameraOn || !this.ws || this.ws.readyState !== WebSocket.OPEN) {
        return;
      }
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      canvas.width = this.$refs.video.videoWidth;
      canvas.height = this.$refs.video.videoHeight;
      ctx.drawImage(this.$refs.video, 0, 0, canvas.width, canvas.height);

      // 转换为 dataURL 用于预览（调试用）
      const dataUrl = canvas.toDataURL("image/jpeg", 0.9);
      this.previewImage = dataUrl; // 将 dataURL 赋值给 data 属性，模板中绑定显示

      // 将视频帧转换为 Blob 并发送给服务器
      canvas.toBlob((blob) => {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          this.ws.send(blob);
        }
      }, "image/jpeg", 0.9);
    }
    ,

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

    // 停止发送视频帧
    stopSendingFrames() {
      this.frameSending = false;
      if (this.requestFrameId) {
        cancelAnimationFrame(this.requestFrameId);
        this.requestFrameId = null;
      }
    }
  },
  mounted() {
    // 页面加载时建立 WebSocket 连接
    this.connectWebSocket();
  },
  beforeUnmount() {
    // 组件销毁前关闭 WebSocket 连接和摄像头
    if (this.ws) {
      this.ws.close();
    }
    this.stopCamera();
  }
};
</script>

<style scoped>
video {
  border: 1px solid #ccc;
  margin-bottom: 20px;
}
button {
  padding: 10px;
  font-size: 16px;
  margin-top: 10px;
  cursor: pointer;
}
</style>
