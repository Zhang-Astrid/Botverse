<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { reactive } from "vue";
import api from "@/api/api.js";
const isLogin = ref(true); // 登录或注册切换状态
const isLoading = ref(false); // 加载状态
const errorMessage = ref(''); // 错误消息
// 登录表单数据
const loginForm = ref({
  username: '',
  password: '',
});

// 注册表单数据
const registerForm = ref({
  username: '',
  password: '',
  gender: 'male', // 默认性别
  birthday: '', // 生日
});

// 切换到登录页面
const switchToLogin = () => {
  isLogin.value = true;
  errorMessage.value = ''; // 清除错误消息
};

// 切换到注册页面
const switchToRegister = () => {
  isLogin.value = false;
  errorMessage.value = ''; // 清除错误消息
};

// 处理登录逻辑
const handleLogin = async () => {
  isLoading.value = true; // 启动加载状态
  errorMessage.value = ''; // 清除错误消息

  try {
    alert(loginForm.value.username);
    const response = await axios.post('http://127.0.0.1:8080/user_sys/login', {
      username: loginForm.value.username,
      password: loginForm.value.password,
    });
    // alert(response.status);
    if (response.status === 200) {
      alert(response.data.message); // 显示成功消息
      // 跳转到其他页面或刷新
      // console.log(this.$router)
      window.location.href = 'http://localhost:5173/main';
    }
    else alert("Unknown Error!")
  } catch (error) {
    console.error(error)
    if (error.response) {
      // 后端返回的错误消息
      errorMessage.value = error.response.data.message;
      alert(errorMessage.value)
    } else {
      errorMessage.value = 'Network error. Please try again later.';
      alert(errorMessage.value)
    }
  } finally {
    isLoading.value = false; // 停止加载状态
  }
};

// 处理注册逻辑
const handleRegister = async () => {
  isLoading.value = true; // 启动加载状态
  errorMessage.value = ''; // 清除错误消息
  
  try {
    const response = await axios.post('http://127.0.0.1:8080/user_sys/register', {
      username: registerForm.value.username,
      password: registerForm.value.password,
      gender: registerForm.value.gender,
      birthday: registerForm.value.birthday,
      image: "https://multiavatar.com/img/logo-animated.gif?v=003",
    });
    // alert(response.status);
    if (response.status === 200) {
      const response_session= await api.post("/chat_sys/create_session",{
        session_name: "New session",
        model_id: 16,
        owner_id: response.data.id,
      })
      alert(response.data.message); // 显示成功消息
      switchToLogin(); // 注册成功后跳转到登录页面
    }
  } catch (error) {
    console.error('Error:', error);
    if (error.response) {
      // 后端返回的错误消息
      errorMessage.value = error.response.data.message;
      alert(errorMessage.value)
    } else {
      errorMessage.value = 'Network error. Please try again later.';
      alert(errorMessage.value)
    }
  } finally {
    isLoading.value = false; // 停止加载状态
  }
};
</script>

<template>
  <div class="auth-container">
    <div class="auth-left">
      <img src="@/img/mainBG.png" alt="Background Image" class="auth-bg" />
    </div>
    <div class="auth-right">
      <div class="auth-box">
        <img src="@/img/logo.png" alt="Logo" class="auth-logo" />
        <h1>Botverse</h1>
        <h3>AI Chat-Bot</h3>

        <!-- 切换登录和注册 -->
        <div class="auth-tabs">
          <div :class="{ active: isLogin }" @click="switchToLogin">Login</div>
          <div :class="{ active: !isLogin }" @click="switchToRegister">Register</div>
        </div>

        <!-- 登录表单 -->
        <form v-if="isLogin" @submit.prevent="handleLogin">
          <div class="input-group">
            <label for="login-username">User name</label>
            <input
                type="text"
                id="login-username"
                v-model="loginForm.username"
                placeholder="Enter your user username"
                required
            />
          </div>
          <div class="input-group">
            <label for="login-password">Password</label>
            <input
                type="password"
                id="login-password"
                v-model="loginForm.password"
                placeholder="Enter your password"
                required
            />
          </div>
          <button
              type="submit"
              class="btn-primary"
              :disabled="isLoading"
          >
            {{ isLoading ? 'Loading...' : 'Sign in' }}
          </button>
        </form>

        <!-- 注册表单 -->
        <form v-else @submit.prevent="handleRegister">
          <div class="input-group">
            <label for="register-username">User name</label>
            <input
                type="text"
                id="register-username"
                v-model="registerForm.username"
                placeholder="Enter your username"
                required
            />
          </div>
          <div class="input-group">
            <label for="register-password">Password</label>
            <input
                type="password"
                id="register-password"
                v-model="registerForm.password"
                placeholder="Enter your password"
                required
            />
          </div>
          <div class="input-group">
            <label for="register-gender">Gender</label>
            <select id="register-gender" v-model="registerForm.gender" class="input-field">
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div class="input-group">
            <label for="register-birthday">Birthday</label>
            <input
                type="date"
                id="register-birthday"
                v-model="registerForm.birthday"
                required
            />
          </div>
          <button
              type="submit"
              class="btn-primary"
              :disabled="isLoading"
          >
            {{ isLoading ? 'Loading...' : 'Sign up' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-container {
  display: flex;
  height: 100vh;
}

.auth-left {
  flex: 1;
  background: #f0f0f0;
}

.auth-bg {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.auth-right {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #ffffff;
}

.auth-box {
  width: 360px;
  text-align: center;
}

.auth-logo {
  width: 60px;
  height: 60px;
  margin-bottom: 16px;
}

.auth-tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.auth-tabs div {
  margin: 0 8px;
  padding: 8px 16px;
  cursor: pointer;
  border-bottom: 2px solid transparent;
}

.auth-tabs .active {
  border-bottom: 2px solid #4c5caf;
  font-weight: bold;
}

.input-group {
  margin-bottom: 16px;
  text-align: left;
}

.input-group label {
  display: block;
  font-size: 14px;
  margin-bottom: 8px;
}

.input-group input,
.input-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn-primary {
  width: 100%;
  padding: 10px;
  background-color: #4c5caf;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-primary:disabled {
  background-color: #d6d6d6;
  cursor: not-allowed;
}
</style>
