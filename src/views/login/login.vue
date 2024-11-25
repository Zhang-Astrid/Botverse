<script setup>
import {useRouter} from "vue-router";

const router = useRouter();
// const goTo = () => {
//   router.push('/register')
// };


import {ref} from 'vue';

const isLogin = ref(true); // 默认显示登录界面
const email = ref('');
const password = ref('');
const errorMessage = ref('');

const toggleLogin = () => {
  isLogin.value = !isLogin.value; // 切换登录/注册状态
  errorMessage.value = ''; // 清空错误信息
};

// 模拟登录/注册操作
const handleSubmit = () => {
  if (!email.value || !password.value) {
    errorMessage.value = '邮箱和密码不能为空';
    return;
  }

  if (isLogin.value) {
    // 模拟登录逻辑
    console.log('登录中...', email.value, password.value);
  } else {
    // 模拟注册逻辑
    console.log('注册中...', email.value, password.value);
  }
};

</script>

<template>
  Login Page
  <!--  <hr>-->
  <!--  <router-link to='/register'>路径传参-Register</router-link>-->
  <!--  <hr>-->
  <!--  <router-link :to="{path:'/user',query:{id:200,title:'vue3'}}">-->
  <!--    查询字符串传参 - 动态属性绑定-->
  <!--  </router-link>-->
  <!--  <hr>-->
  <!--  <button @click="goTo">编程式导航</button>-->
  <!--  <hr>-->

  <div class="login-container">
    <h2>{{ isLogin ? '登录' : '注册' }}</h2>

    <!-- 邮箱输入框 -->
    <div class="input-group">
      <label for="email">邮箱</label>
      <input
          type="email"
          id="email"
          v-model="email"
          placeholder="请输入您的邮箱"
          required
      />
    </div>

    <!-- 密码输入框 -->
    <div class="input-group">
      <label for="password">密码</label>
      <input
          type="password"
          id="password"
          v-model="password"
          placeholder="请输入您的密码"
          required
      />
    </div>

    <!-- 错误信息显示 -->
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <!-- 提交按钮 -->
    <button @click="handleSubmit">{{ isLogin ? '登录' : '注册' }}</button>

    <!-- 切换登录与注册 -->
    <p class="toggle">
      {{ isLogin ? '没有账户？' : '已有账户？' }}
      <span @click="toggleLogin">{{ isLogin ? '注册' : '登录' }}</span>
    </p>
  </div>

</template>


<style scoped>
.login-container {
  width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #fafafa;
}

h2 {
  text-align: center;
}

.input-group {
  margin-bottom: 16px;
}

input {
  width: 100%;
  padding: 8px;
  margin-top: 4px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #4c5caf;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #4c5caf;
}

.error-message {
  color: #ff0707;
  font-size: 14px;
  margin-bottom: 8px;
  text-align: center;
}

.toggle {
  text-align: center;
  margin-top: 16px;
  color: #666;
  cursor: pointer;
}

.toggle span {
  color: #4c5caf;
  font-weight: bold;
}
</style>