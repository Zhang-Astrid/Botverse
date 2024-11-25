<script setup>
import axios from 'axios';
import { ref } from 'vue';

const isLogin = ref(true); // 登录或注册切换
const isLoading = ref(false); // 加载状态

// 登录表单数据
const loginForm = ref({
  id: '', // 用户 ID
  password: '', // 密码
});

// 注册表单数据
const registerForm = ref({
  username: '', // 用户名
  password: '', // 密码
  gender: 'male', // 性别
  birthday: '', // 生日
  isAdmin: false, // 是否为管理员
});

// 切换到登录页面
const switchToLogin = () => {
  isLogin.value = true;
};

// 切换到注册页面
const switchToRegister = () => {
  isLogin.value = false;
};

// 处理登录逻辑
const handleLogin = async () => {
  if (isLoading.value) return; // 如果正在加载，则不重复请求
  isLoading.value = true; // 设置加载状态

  try {
    const response = await axios.post('http://127.0.0.1:5000/login', {
      id: loginForm.value.id,
      password: loginForm.value.password,
    });

    if (response.data.success) {
      alert('Login successful!');
    } else {
      alert(response.data.message);
    }
  } catch (error) {
    console.error(error);
    alert('Error logging in. Please try again.');
  } finally {
    isLoading.value = false; // 加载完成
  }
};

// 处理注册逻辑
const handleRegister = async () => {
  if (isLoading.value) return; // 如果正在加载，则不重复请求
  isLoading.value = true; // 设置加载状态

  try {
    const response = await axios.post('http://127.0.0.1:5000/register', {
      username: registerForm.value.username,
      password: registerForm.value.password,
      gender: registerForm.value.gender,
      birthday: registerForm.value.birthday,
      isAdmin: registerForm.value.isAdmin,
    });

    if (response.data.success) {
      alert('Registration successful!');
      isLogin.value = true; // 切换到登录页面
    } else {
      alert(response.data.message);
    }
  } catch (error) {
    console.error(error);
    alert('Error registering. Please try again.');
  } finally {
    isLoading.value = false; // 加载完成
  }
};
</script>

<template>
  <div class="auth-container">
    <div class="auth-left">
      <img src="@/img/chat_botBG.png" alt="Background Image" class="auth-bg" />
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
            <label for="login-id">User ID</label>
            <input
                type="text"
                id="login-id"
                v-model="loginForm.id"
                placeholder="Enter your user ID"
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
  border-bottom: 2px solid #007bff;
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
  background-color: #007bff;
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
