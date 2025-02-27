<template>
  <div>
    <div v-if="!isLoggedIn">
      <!-- 登录部分 -->
      <div v-if="!isRegistering">
        <h2>登录</h2>
        <input v-model="username" placeholder="用户名" />
        <input v-model="password" type="password" placeholder="密码" />
        <button @click="login">登录</button>

        <div v-if="loginErrorMessage">{{ loginErrorMessage }}</div>

        <p>还没有账户？ <button @click="switchToRegister">注册</button></p>
      </div>

      <!-- 注册部分 -->
      <div v-if="isRegistering">
        <h2>注册</h2>
        <input v-model="newUsername" placeholder="用户名" />
        <input v-model="newPassword" type="password" placeholder="密码" />
        <input v-model="email" placeholder="邮箱" />
        <button @click="register">注册</button>

        <div v-if="registerErrorMessage">{{ registerErrorMessage }}</div>

        <p>已有账户？ <button @click="switchToLogin">登录</button></p>
      </div>
    </div>

    <!-- 主页内容 -->
    <div v-if="isLoggedIn">
      <h2>欢迎，{{ username }}！</h2>
      <button @click="logout">退出</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      newUsername: "",
      newPassword: "",
      email: "",
      isLoggedIn: false,
      isRegistering: false, // 控制是否显示注册表单
      registerErrorMessage: "",
      loginErrorMessage: "",
    };
  },
  methods: {
    // 登录方法
    async login() {
      try {
        const response = await axios.post("http://localhost:8080/api/users/login", {
          username: this.username,
          password: this.password
        });

        if (response.status === 200) {
          this.isLoggedIn = true;
          this.username = response.data.username; // 假设后端返回用户信息
          localStorage.setItem("isLoggedIn", "true"); // 使用 localStorage 记录登录状态
          console.log("登录成功");
        } else {
          this.loginErrorMessage = "登录失败，请检查用户名或密码";
        }
      } catch (error) {
        console.error("登录请求错误", error);
        this.loginErrorMessage = "登录请求失败，请检查网络";
      }
    },

    // 注册方法
    async register() {
      try {
        const requestData = {
          username: this.newUsername,
          password: this.newPassword,
          email: this.email
        };

        const response = await axios.post("http://localhost:8080/api/users/register", requestData, {
          headers: {
            "Content-Type": "application/json",
          }
        });

        if (response.status === 200) {
          console.log("注册成功", response.data);
          this.loginErrorMessage = "注册成功，请登录！";
        } else {
          this.registerErrorMessage = "注册失败，请重试";
        }
      } catch (error) {
        console.error("注册请求错误", error); // 详细错误
        this.registerErrorMessage = "注册请求失败，请检查网络";
      }
    },

    // 切换到注册页面
    switchToRegister() {
      this.isRegistering = true;
      this.loginErrorMessage = "";
      this.registerErrorMessage = "";
    },

    // 切换到登录页面
    switchToLogin() {
      this.isRegistering = false;
      this.loginErrorMessage = "";
      this.registerErrorMessage = "";
    },

    // 退出方法
    logout() {
      this.isLoggedIn = false;
      this.username = "";
      localStorage.removeItem("isLoggedIn"); // 清除登录状态
      console.log("退出成功");
    }
  },
  mounted() {
    // 页面加载时检查登录状态
    const storedLoginStatus = localStorage.getItem("isLoggedIn");
    if (storedLoginStatus === "true") {
      this.isLoggedIn = true; // 如果有登录状态，则自动设置为已登录
    }
  }
};
</script>

<style scoped>
/* 可以根据需要自定义样式 */
</style>
