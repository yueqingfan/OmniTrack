<template>
  <div>
    <h1>实时视频</h1>
    <video ref="video" width="640" height="480" autoplay></video>
    <div>
      <button @click="toggleCamera">{{ isCameraOn ? '关闭摄像头' : '开启摄像头' }}</button>
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
    };
  },
  methods: {
    connectWebSocket() {
      if (this.ws) {
        this.ws.close();
      }
      this.ws = new WebSocket("ws://localhost:8080/video-stream");

      this.ws.onopen = () => {
        console.log("Connected to WebSocket server");
      };

      this.ws.onerror = (error) => {
        console.error("WebSocket error: ", error);
      };

      this.ws.onclose = () => {
        console.log("Disconnected from WebSocket server, attempting reconnect...");
        setTimeout(this.connectWebSocket, 3000); // 3秒后尝试重连
      };
    },

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

    stopCamera() {
      if (this.videoStream) {
        this.videoStream.getTracks().forEach(track => track.stop());
        this.videoStream = null;
        this.isCameraOn = false;
      }
      this.stopSendingFrames();
    },

    toggleCamera() {
      if (this.isCameraOn) {
        this.stopCamera();
      } else {
        this.startCamera();
      }
    },

    sendVideoFrame() {
      if (!this.isCameraOn || !this.ws || this.ws.readyState !== WebSocket.OPEN) {
        return;
      }
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      canvas.width = this.$refs.video.videoWidth;
      canvas.height = this.$refs.video.videoHeight;
      ctx.drawImage(this.$refs.video, 0, 0, canvas.width, canvas.height);

      canvas.toBlob((blob) => {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          this.ws.send(blob);
        }
      }, "image/jpeg", 0.9);
    },

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

    stopSendingFrames() {
      this.frameSending = false;
      if (this.requestFrameId) {
        cancelAnimationFrame(this.requestFrameId);
        this.requestFrameId = null;
      }
    },
  },

  mounted() {
    this.connectWebSocket();
  },

  beforeUnmount() {
    if (this.ws) {
      this.ws.close();
    }
    this.stopCamera();
  },
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
