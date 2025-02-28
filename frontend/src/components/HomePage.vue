<template>
  <div class="home-container">
    <div class="login-box">
      <div class="text-center avatar-box">
        <img src="../assets/logo.png" class="img-thumbnail avatar" alt="Logo">
      </div>
      <div class="form-login-container">
        <div v-if="!isRegistering" class="form-login p-4">
          <h2 class="form-title">登录</h2>
          <div class="form-group">
            <label for="username">账号</label>
            <input
                type="text"
                class="form-control"
                id="username"
                placeholder="请输入账号"
                autocomplete="off"
                v-model.trim="username"
            />
          </div>
          <div class="form-group">
            <label for="password">密码</label>
            <input
                type="password"
                class="form-control"
                id="password"
                placeholder="请输入密码"
                v-model.trim="password"
            />
          </div>
          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="switchToRegister">注册</button>
            <button type="button" class="btn btn-primary" @click="login">登录</button>
          </div>
          <div v-if="loginError" class="error-message">{{ loginError }}</div>
        </div>
        <div v-if="isRegistering" class="form-login p-4">
          <h2 class="form-title">注册</h2>
          <div class="form-group">
            <label for="newUsername">用户名</label>
            <input
                type="text"
                class="form-control"
                id="newUsername"
                placeholder="请输入用户名"
                v-model.trim="newUsername"
            />
          </div>
          <div class="form-group">
            <label for="newPassword">密码</label>
            <input
                type="password"
                class="form-control"
                id="newPassword"
                placeholder="请输入密码"
                v-model.trim="newPassword"
            />
          </div>
          <div class="form-group">
            <label for="email">邮箱</label>
            <input
                type="email"
                class="form-control"
                id="email"
                placeholder="请输入邮箱"
                v-model.trim="email"
            />
          </div>
          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="login">登录</button>
            <button type="button" class="btn btn-primary" @click="register">注册</button>
          </div>
          <div v-if="registerError" class="error-message">{{ registerError }}</div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
export default {
  mounted() {
    console.log("Vue 组件已加载");
  },
  data() {
    return {
      username: "",
      password: "",
      newUsername: "",
      newPassword: "",
      email: "",
      isRegistering: false,
      loginError: "",
      registerError: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://localhost:8080/api/users/login", {
          username: this.username,
          password: this.password,
        });
        if (response.status === 200) {
          console.log("登录成功");
          this.$router.push('/dashboard');
        } else {
          console.log("响应状态非200，登录失败");
          this.loginError = "登录失败，请检查用户名或密码";
        }
      } catch (error) {
        console.error("登录请求错误", error);
        this.loginError = "登录请求失败，请检查网络";
      }
    },
    async register() {
      try {
        const requestData = {
          username: this.newUsername,
          password: this.newPassword,
          email: this.email,
        };
        const response = await axios.post("http://localhost:8080/api/users/register", requestData, {
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (response.status === 200) {
          console.log("注册成功", response.data);
          this.switchToLogin();
        } else {
          this.registerError = "注册失败，请重试";
        }
      } catch (error) {
        console.error("注册请求错误", error);
        this.registerError = "注册请求失败，请检查网络";
      }
    },
    switchToRegister() {
      this.isRegistering = true;
      this.loginError = "";
      this.registerError = "";
    },
    switchToLogin() {
      this.isRegistering = false;
      this.loginError = "";
      this.registerError = "";
    },
  },
};
</script>

<style lang="less" scoped>
.home-container {
  background-color: #35495e;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-box {
  width: 400px;
  background-color: #fff;
  border-radius: 15px;
  padding: 40px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  position: relative;
}
.avatar-box {
  position: absolute;
  top: -60px;
  left: 50%;
  transform: translateX(-50%);
}
.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.2);
}
.form-login-container {
  display: flex;
  flex-direction: column;
}
.form-title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 22px;
}
.form-group {
  margin-bottom: 20px;
}
label {
  font-size: 14px;
  color: #333;
}
.form-control {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: 16px;
  transition: border-color 0.3s;
}
.form-control:focus {
  border-color: #007bff;
  outline: none;
}
.form-actions {
  display: flex;
  justify-content: space-between;
}
.btn {
  width: 48%;
  padding: 10px;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
}
.btn-primary:hover {
  background-color: #0056b3;
}
.btn-secondary {
  background-color: #6c757d;
  color: white;
  border: none;
}
.btn-secondary:hover {
  background-color: #5a6268;
}
.error-message {
  color: red;
  margin-top: 10px;
  font-size: 14px;
  text-align: center;
}
</style>
