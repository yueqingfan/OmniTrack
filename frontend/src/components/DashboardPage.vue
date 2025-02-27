<template>
  <div class="dashboard">
    <h2>欢迎，{{ username }}</h2>
    <div>
      <h3>系统状态</h3>
      <p>这是一个公共安全监控系统的主界面。</p>

      <!-- 示例：显示一些统计数据 -->
      <div class="stats">
        <h4>当前监控状态</h4>
        <ul>
          <li>总检测目标数: {{ totalTargets }}</li>
          <li>当前在线用户: {{ onlineUsers }}</li>
        </ul>
      </div>

      <button @click="logout">退出登录</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: localStorage.getItem('username') || '用户',  // 从 localStorage 获取用户名
      totalTargets: 0,
      onlineUsers: 0
    };
  },
  mounted() {
    this.fetchDashboardData();  // 加载实时数据
  },
  methods: {
    fetchDashboardData() {
      // 假设从后端获取监控数据
      // 示例：模拟从后端 API 获取统计数据
      this.totalTargets = 123;  // 假设的数据
      this.onlineUsers = 50;    // 假设的数据
    },
    logout() {
      // 清除 token 和用户信息
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      this.$router.push('/login');  // 跳转到登录页面
    }
  }
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
  font-family: Arial, sans-serif;
}

.stats {
  margin-top: 20px;
}

button {
  margin-top: 20px;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
