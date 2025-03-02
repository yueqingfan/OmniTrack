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
            <small v-if="loginErrors.username" class="error-message">{{ loginErrors.username }}</small>
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
            <small v-if="loginErrors.password" class="error-message">{{ loginErrors.password }}</small>
          </div>

          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="switchToRegister">注册</button>
            <button type="button" class="btn btn-primary" @click="login">登录</button>
          </div>

          <div v-if="loginErrors.general" class="error-message">{{ loginErrors.general }}</div>
        </div>

        <div v-if="isRegistering" class="form-login p-4">
          <h2 class="form-title">注册</h2>

          <div class="form-group">
            <label for="newUsername">用户名</label>
            <input
                type="text"
                class="form-control"
                id="newUsername"
                placeholder="请输入用户名 (6-20个字符)"
                v-model.trim="newUsername"
            />
            <small v-if="registerErrors.username" class="error-message">{{ registerErrors.username }}</small>
          </div>

          <div class="form-group">
            <label for="newPassword">密码</label>
            <input
                type="password"
                class="form-control"
                id="newPassword"
                placeholder="请输入密码 (至少6个字符)"
                v-model.trim="newPassword"
            />
            <small v-if="registerErrors.password" class="error-message">{{ registerErrors.password }}</small>
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
            <small v-if="registerErrors.email" class="error-message">{{ registerErrors.email }}</small>
          </div>

          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="switchToLogin">登录</button>
            <button type="button" class="btn btn-primary" @click="register">注册</button>
          </div>

          <div v-if="registerErrors.general" class="error-message">{{ registerErrors.general }}</div>
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
      loginErrors: {
        username: "",
        password: "",
        general: ""
      },
      registerErrors: {
        username: "",
        password: "",
        email: "",
        general: ""
      }
    };
  },
  methods: {
    validateLoginForm() {
      let isValid = true;
      this.loginErrors = { username: "", password: "", general: "" };

      if (!this.username) {
        this.loginErrors.username = "用户名不能为空";
        isValid = false;
      } else if (this.username.length < 6 || this.username.length > 20) {
        this.loginErrors.username = "用户名长度必须在6到20个字符之间";
        isValid = false;
      }

      if (!this.password) {
        this.loginErrors.password = "密码不能为空";
        isValid = false;
      } else if (this.password.length < 6) {
        this.loginErrors.password = "密码长度至少6个字符";
        isValid = false;
      }

      return isValid;
    },

    validateRegisterForm() {
      let isValid = true;
      this.registerErrors = { username: "", password: "", email: "", general: "" };

      if (!this.newUsername) {
        this.registerErrors.username = "用户名不能为空";
        isValid = false;
      } else if (this.newUsername.length < 6 || this.newUsername.length > 20) {
        this.registerErrors.username = "用户名长度必须在6到20个字符之间";
        isValid = false;
      }

      if (!this.newPassword) {
        this.registerErrors.password = "密码不能为空";
        isValid = false;
      } else if (this.newPassword.length < 6) {
        this.registerErrors.password = "密码长度至少6个字符";
        isValid = false;
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!this.email) {
        this.registerErrors.email = "邮箱不能为空";
        isValid = false;
      } else if (!emailRegex.test(this.email)) {
        this.registerErrors.email = "邮箱格式不正确";
        isValid = false;
      }

      return isValid;
    },

    async login() {
      if (!this.validateLoginForm()) {
        return;
      }

      try {
        const response = await axios.post("http://localhost:8080/api/users/login", {
          username: this.username,
          password: this.password,
        });

        if (response.status === 200) {
          console.log("登录成功");
          this.$router.push('/dashboard');
        }
      } catch (error) {
        console.error("登录请求错误", error);

        if (error.response && error.response.data) {
          // Handle validation errors from server
          if (error.response.status === 400 && typeof error.response.data === 'object') {
            // Map backend validation errors to form fields
            const fieldErrors = error.response.data;
            Object.keys(fieldErrors).forEach(key => {
              if (Object.prototype.hasOwnProperty.call(this.loginErrors, key)) {
                this.loginErrors[key] = fieldErrors[key];
              }
            });
          } else if (error.response.data.message) {
            this.loginErrors.general = error.response.data.message;
          } else {
            this.loginErrors.general = "登录失败，请检查用户名或密码";
          }
        } else {
          this.loginErrors.general = "登录请求失败，请检查网络";
        }
      }
    },

    async register() {
      if (!this.validateRegisterForm()) {
        return;
      }

      try {
        const requestData = {
          username: this.newUsername,
          password: this.newPassword,
          email: this.email,
        };

        const response = await axios.post("http://localhost:8080/api/users/register", requestData);

        if (response.status === 200) {
          alert("注册成功");
          this.switchToLogin();
        }
      } catch (error) {
        console.error("注册请求错误", error);

        if (error.response && error.response.data) {
          if (error.response.status === 400 && typeof error.response.data === 'object') {
            const fieldErrors = error.response.data;
            Object.keys(fieldErrors).forEach(key => {
              if (Object.prototype.hasOwnProperty.call(this.registerErrors, key)) {
                this.registerErrors[key] = fieldErrors[key];
              }
            });
          } else if (error.response.data.message) {
            this.registerErrors.general = error.response.data.message;
          } else {
            this.registerErrors.general = "注册失败";
          }
        } else {
          this.registerErrors.general = "注册请求失败，请检查网络";
        }
      }
    },

    switchToRegister() {
      this.isRegistering = true;
      this.loginErrors = { username: "", password: "", general: "" };
      this.registerErrors = { username: "", password: "", email: "", general: "" };
    },

    switchToLogin() {
      this.isRegistering = false;
      this.loginErrors = { username: "", password: "", general: "" };
      this.registerErrors = { username: "", password: "", email: "", general: "" };
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
  margin-top: 4px;
  font-size: 14px;
  display: block;
}
</style>