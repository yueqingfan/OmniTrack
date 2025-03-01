<template>
  <div>
    <h1>实时视频</h1>
    <video ref="video" width="640" height="480" autoplay></video>
  </div>
</template>

<script>
export default {
  name: "VideoStream",
  data() {
    return {
      ws: null,
      videoStream: null,
    };
  },
  methods: {
    // 连接到 WebSocket 服务
    connectWebSocket() {
      this.ws = new WebSocket("ws://localhost:8080/video-stream"); // 你的 WebSocket 服务器地址

      this.ws.onopen = () => {
        console.log("Connected to WebSocket server");
      };

      this.ws.onerror = (error) => {
        console.error("WebSocket error: ", error);
      };

      this.ws.onclose = () => {
        console.log("Disconnected from WebSocket server");
      };

      this.ws.onmessage = (event) => {
        console.log("Received from server:", event.data);
      };
    },

    // 获取摄像头的视频流
    startCamera() {
      navigator.mediaDevices
          .getUserMedia({ video: true })
          .then((stream) => {
            this.videoStream = stream;
            this.$refs.video.srcObject = stream;
            this.$refs.video.play();
          })
          .catch((err) => {
            console.error("Error accessing camera: " + err);
          });
    },

    // 发送视频帧到 WebSocket
    sendVideoFrame() {
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");

      canvas.width = this.$refs.video.videoWidth;
      canvas.height = this.$refs.video.videoHeight;
      ctx.drawImage(this.$refs.video, 0, 0, canvas.width, canvas.height);

      canvas.toBlob((blob) => {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          this.ws.send(blob); // 发送视频帧
        }
      }, "image/jpeg", 0.9);
    },

    // 每隔 100 毫秒发送一次视频帧
    startSendingFrames() {
      setInterval(this.sendVideoFrame, 100);
    },
  },

  mounted() {
    this.connectWebSocket(); // 连接 WebSocket
    this.startCamera(); // 启动摄像头
    this.startSendingFrames(); // 开始发送视频帧
  },

  beforeUnmount() {
    if (this.ws) {
      this.ws.close();
    }
    if (this.videoStream) {
      this.videoStream.getTracks().forEach(track => track.stop()); // 停止视频流
    }
  }
};
</script>

<style scoped>
video {
  border: 1px solid #ccc;
  margin-bottom: 20px;
}
</style>
