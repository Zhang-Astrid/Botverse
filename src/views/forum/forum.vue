<template>
  <div id="app">
    <!-- 顶部导航栏 -->
    <div class="top-navbar">
      <h1>Forum</h1>
    </div>

    <div class="main-container">
      <!-- 左侧导航栏 -->
      <div class="sidebar">
        <h2>Forums</h2>
        <button class="btn" @click="showCreateForum = true">Create Forum</button>
        <ul>
          <li v-for="forum in forums" :key="forum.id" @click="selectForum(forum)">
            {{ forum.title }}
          </li>
        </ul>
      </div>

      <!-- 右侧内容区域 -->
      <div class="content">
        <div v-if="selectedForum">
          <h2>{{ selectedForum.title }}</h2>
          <p>Created by User {{ selectedForum.owner_id }} on {{ selectedForum.created_at }}</p>

          <!-- 创建日志按钮 -->
          <button class="btn" @click="showCreateLog = true">Create Log</button>

          <!-- 日志列表 -->
          <div class="logs">
            <h3>Logs</h3>
            <div v-for="log in selectedForum.logs" :key="log.id" class="log-item">
              <p><strong>Role:</strong> {{ log.role }}</p>
              <p>{{ log.message }}</p>
              <p><small>{{ log.time }}</small></p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建论坛弹窗 -->
    <div v-if="showCreateForum" class="modal">
      <div class="modal-content">
        <!-- 关闭按钮 -->
        <button class="close-btn" @click="showCreateForum = false">
          &times;
        </button>
        <h2>Create a Forum</h2>
        <form @submit.prevent="createForum">
          <label for="forum-title">Title:</label>
          <input type="text" id="forum-title" v-model="newForum.title" required />
          <br/>

          <!-- Target ID 选择题 -->
          <label for="forum-target-type">Target ID Type: </label>
          <select id="forum-target-type" v-model="targetType" @change="handleTargetTypeChange" required>
            <option value="" disabled>Select Type</option>
            <option value="chatbot">Chatbot</option>
            <option value="user">User</option>
          </select>
          <br />

          <!-- Chatbot 多选 -->
          <div v-if="targetType === 'chatbot'">
            <label for="chatbot-selection">Select Chatbot:</label>
            <select id="chatbot-selection" v-model="newForum.targetId" required>
              <option v-for="chatbot in chatbots" :value="chatbot.id" :key="chatbot.id">
                {{ chatbot.name }}
              </option>
            </select>
          </div>

          <!-- User 填空框 -->
          <div v-if="targetType === 'user'">
            <label for="user-id">Enter User ID:</label>
            <input
                type="text"
                id="user-id"
                v-model="newForum.targetId"
                required
                @blur="validateUserId"
            />
            <span v-if="userIdError" class="error">{{ userIdError }}</span>
          </div>

          <br />
          <button type="submit" class="btn">Create Forum</button>
        </form>
      </div>
    </div>



    <!-- 创建日志弹窗 -->
    <div v-if="showCreateLog" class="modal">
      <div class="modal-content">
        <!-- 关闭按钮 -->
        <button class="close-btn" @click="showCreateLog = false">
          &times;
        </button>
        <h2>Create a Log</h2>
        <form @submit.prevent="createLog">
          <label for="log-message">Message:</label>
          <textarea id="log-message" v-model="newLog.message" required></textarea>
          <br>
          <button type="submit" class="btn">Create Log</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      currentUserId: 1, // 当前用户ID
      newLog: {
        message: '',
      },
      forums: [], // 论坛列表
      selectedForum: null, // 当前选中的论坛
      showCreateLog: false, // 创建日志弹窗的显示状态
      showCreateForum: false, // 控制弹窗显示
      newForum: {
        title: '',
        targetId: ''
      },
      targetType: '', // 存储 Target ID 类型（chatbot 或 user）
      chatbots: [], // 用于存储从后台加载的 Chatbot 名称
      userIdError: '', // 用户ID验证错误信息
    };
  },
  methods: {
    // 获取后台论坛列表
    getForums() {
      axios.get('/api/forums') // 向后端发起请求
          .then(response => {
            this.forums = response.data; // 将返回的论坛数据存储到 forums 中
          })
          .catch(error => {
            console.error('Error fetching forums:', error);
          });
    },

    // 选择论坛
    selectForum(forum) {
      this.selectedForum = forum;
    },

    // 切换 Target ID 类型时执行
    handleTargetTypeChange() {
      if (this.targetType === 'chatbot') {
        this.loadChatbots(); // 加载 Chatbot 名称
      }
    },

    // 加载 Chatbot 列表（模拟从后台加载）
    loadChatbots() {
      // 假设后端返回的数据是以下形式
      this.chatbots = [
        { id: 'chatgpt-4o', name: 'ChatGPT-4' },
        { id: 'chatgpt-mini', name: 'ChatGPT-Mini' },
        { id: 'chatgpt-3.5', name: 'ChatGPT-3' }
      ];
    },

    // 验证 User ID 是否存在
    async validateUserId() {
      const userId = this.newForum.targetId;
      if (userId) {
        try {
          const response = await axios.get(`/api/validate-user/${userId}`);
          if (response.data.exists) {
            this.userIdError = ''; // 如果用户存在，清除错误信息
          } else {
            this.userIdError = 'User ID does not exist';
          }
        } catch (error) {
          this.userIdError = 'Error validating User ID';
        }
      }
    },

    // 提交创建论坛表单
    async createForum() {
      try {
        // 假设这里会将表单数据提交给后端
        const response = await axios.post('/api/create-forum', this.newForum);
        console.log('Forum created:', response.data);
        this.showCreateForum = false; // 成功后关闭弹窗
      } catch (error) {
        console.error('Error creating forum:', error);
      }
    },

    // 创建日志
    createLog() {
      if (!this.selectedForum) {
        console.error('No forum selected!');
        return;
      }

      const newLogData = {
        post_id: this.selectedForum.id,
        role: this.currentUserId,
        message: this.newLog.message,
        time: new Date().toISOString(),
      };

      axios.post('/api/posts/logs', newLogData)
          .then(response => {
            this.selectedForum.logs.push(response.data); // 将新日志加入到选中的论坛日志中
            this.showCreateLog = false;
            this.newLog.message = '';
          })
          .catch(error => {
            console.error('Error posting log:', error);
          });
    },
  },

  mounted() {
    this.getForums(); // 页面加载时获取论坛列表
  },
};
</script>

<style scoped>
#app {
  font-family: 'Arial', sans-serif;
}

.top-navbar {
  background-color: #333;
  color: white;
  padding: 15px;
  text-align: center;
  font-size: 1.5em;
}

.main-container {
  display: flex;
  margin-top: 20px;
}

.sidebar {
  width: 250px;
  background-color: #f5f5f5;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar h2 {
  font-size: 1.2em;
  margin-top: 20px;
}

.sidebar ul {
  list-style-type: none;
  padding: 0;
}

.sidebar ul li {
  height: 20px;
  cursor: pointer;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-top: 10px;
}

.sidebar ul li:hover {
  background-color: #f0f0f0;
}

.content {
  flex-grow: 1;
  padding: 20px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  background-color: white;
}

h2 {
  color: #333;
}
/* 弹窗的背景 */
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* 半透明背景 */
  z-index: 1000; /* 确保弹窗在最上层 */
}

/* 弹窗的内容区域 */
.modal-content {
  position: relative;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-width: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 15px; /* 控制表单元素之间的间距 */
}

/* 表单标签和输入框容器 */
.form-group {
  display: flex;
  flex-direction: column;
}

/* 标签 */
label {
  font-size: 1em;
  margin-bottom: 5px;
}

/* 输入框和选择框 */
input, select, textarea {
  height: 35px; /* 设置所有输入框和选择框的高度一致 */
  padding: 8px;
  font-size: 1em;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

/* 文本区域 */
textarea {
  height: 100px; /* 为文本区域设置较高的高度 */
  resize: none; /* 禁用调整大小 */
}

/* 关闭按钮样式 */
.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 2em;
  cursor: pointer;
  background: transparent;
  border: none;
  color: #888;
}

.close-btn:hover {
  color: #f00; /* 鼠标悬停时改变颜色 */
}

/* 错误提示 */
.error {
  color: red;
  font-size: 0.9em;
  margin-top: 5px;
}

/* 日志内容的输入框样式 */
textarea {
  width: 100%;
  height: 150px;
  padding: 8px;
  margin: 8px 0;
  border-radius: 4px;
  border: 1px solid #ccc;
  box-sizing: border-box;
  resize: vertical; /* 允许用户调整文本框高度 */
}

/* 提交按钮样式 */
button[type="submit"] {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button[type="submit"]:hover {
  background-color: #0056b3;
}

/* 输入框和按钮的样式 */
input[type="text"] {
  max-width: 330px;
  width: 100%;
  padding: 8px;
  margin: 8px 0;
  border-radius: 4px;
  border: 1px solid #ccc;
}

button[type="submit"] {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button[type="submit"]:hover {
  background-color: #0056b3;
}

h3 {
  font-size: 1.2em;
}

.logs {
  margin-top: 20px;
}

.log-item {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 6px;
}

.log-item p {
  margin: 5px 0;
}

h2, .btn {
  display: inline-block; /* 使它们在一行 */
  margin-right: 40px; /* 设置两个元素之间的间距 */
}
</style>
