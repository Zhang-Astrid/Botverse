<template>
  <div id="app">
    <!-- 顶部导航栏 -->
    <div class="top-navbar">
      <h1>Forum</h1>
    </div>

    <div class="main-container">
      <!-- 左侧导航栏 -->
      <div class="sidebar">
        <!--        <h2>Forums</h2>-->
        <div class="search-container">
          <!-- 筛选条件选择框 -->
          Search
          <select v-model="searchBy" class="search-select">
            <option value="owner_id">Owner</option>
            <option value="target_id">Target user</option>

          </select>

          <!-- 根据筛选条件显示输入框 -->
          <input
              type="text"
              v-model="searchQuery"
              placeholder="Input ID"
              class="search-input"
          />

          <!-- 搜索按钮 -->
          <button @click="performSearch"
                  :class="['search-button', { 'active': isButtonActive }]">
            <img src="@/img/searchInForum.png" alt="Search" class="search-icon"/>
          </button>
        </div>

        <div class="button-container">
          <button class="btn" @click="showCreateForum = true">Create Forum</button>
        </div>
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
          <h4>{{ selectedForum.content }}</h4>
          <p>Created by User {{ selectedForum.owner_id }} on {{ selectedForum.created_at }}</p>

          <!-- 创建日志按钮 -->
          <button class="btn" @click="showCreateLog = true">Create Log</button>

          <!-- 日志列表 -->
          <div class="logs">
            <h3>Logs</h3>
            <div v-for="log in selectedForum.logs" :key="log.id" class="log-item">
              <p><strong>{{ log.sender_name }}</strong> </p>
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
          <input type="text" id="forum-title" v-model="newForum.title" required/>
          <br/>

          <!-- Target ID 选择题 -->
          <label for="forum-target-type">Target ID Type: </label>
          <select id="forum-target-type" v-model="targetType" @change="handleTargetTypeChange" required>
            <option value="" disabled>Select Type</option>
            <option value="model">Model</option>
            <option value="user">User</option>
          </select>
          <br/>

          <!-- Chatbot 多选 -->
          <div v-if="targetType === 'model'">
            <label for="model-id">Enter Model ID:</label>
            <input
                type="text"
                id="model-id"
                v-model="newForum.targetId"
                required
                @blur="validateModelId"
            />
            <span v-if="modelIdError" class="error">{{ modelIdInfo }}</span>
            <span v-else class="correct">{{ modelIdInfo }}</span>
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
            <span v-if="userIdError" class="error">{{ userIdInfo }}</span>
            <span v-else class="correct">{{ userIdInfo }}</span>
          </div>

          <!-- 内容输入框 -->
          <label for="forum-content">Content:</label>
          <textarea id="forum-content" v-model="newForum.content" required></textarea>
          <br/>

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
import api from "@/api/api.js";

export default {
  data() {
    return {
      isButtonActive: false, // 按钮是否被激活
      currentUserId: 1, // 当前用户ID
      newLog: {
        message: '',
      },
      searchBy: 'owner_id',  // 默认筛选 Owner ID
      searchQuery: '',       // 搜索内容
      // 预设测试数据
      forums: [
        {
          id: 1,
          title: 'Technology Forum',
          owner_id: 1,
          created_at: '2024-12-01',
          logs: [
            {id: 1, role: 'User', message: 'Welcome to the forum!', time: '2024-12-01T10:00:00Z'},
            {id: 2, role: 'Admin', message: 'Rules have been updated.', time: '2024-12-02T12:00:00Z'},
          ],
          content:'test content.'
        },
        {
          id: 2,
          title: 'Health Forum',
          owner_id: 2,
          created_at: '2024-11-15',
          logs: [
            {id: 1, role: 'Moderator', message: 'New guidelines posted.', time: '2024-11-16T14:00:00Z'},
          ],
          content:'test content.'
        }
      ],
      filteredForums: [], // 存储过滤后的论坛
      selectedForum: {
        id: 0,
        title: "",
        owner_id: 0,
        created_at: null,
        target_id: 0,
        target_type: 0,
        logs: [ ],
        content:null
      }, // 当前选中的论坛
      showCreateLog: false, // 创建日志弹窗的显示状态
      showCreateForum: false, // 控制弹窗显示
      newForum: {
        title: '',
        targetId: '',
        content: '' // Add the content property
      },
      targetType: '', // 存储 Target ID 类型（chatbot 或 user）
      chatbots: [], // 用于存储从后台加载的 Chatbot 名称
      userIdError: false, // 用户ID验证错误信息
      userIdInfo: '',
      modelIdError: false, // 用户ID验证错误信息
      modelIdInfo: '',
    };
  },
  async created(){
    const current_info = await axios.post('http://127.0.0.1:8080/user_sys/acquire_current_user',
          {}
      );
    this.currentUserId=current_info.data.user_id
    await this.loadAllForum()
  },
  methods: {
    // 搜索操作
    performSearch() {
      this.isButtonActive = !this.isButtonActive; // 切换状态
      if (this.searchQuery.trim() === '') {
        this.filteredForums = this.forums;  // 如果没有输入内容，展示所有论坛
      } else {
        this.filteredForums = this.forums.filter(forum => {
          if (this.searchBy === 'owner_id') {
            return forum.owner_id && forum.owner_id.toString().includes(this.searchQuery);
          } else if (this.searchBy === 'target_id') {
            return forum.target_id && forum.target_id.toString().includes(this.searchQuery);
          }
          return false;
        });
      }
    },
    // 获取后台论坛列表

    // 选择论坛
    async selectForum(forum) {
      this.selectedForum = forum;
      await this.loadCurrentForumLog()
    },

    // 切换 Target ID 类型时执行
    handleTargetTypeChange() {
      this.newForum.targetId = ""
    },

    // 验证 User ID 是否存在
    async validateUserId() {
      const userId = this.newForum.targetId;
      if (userId) {
        try {
          const response = await api.post("/user_sys/user", {
            user_id: userId
          });
          this.userIdError = false
          this.userIdInfo = response.data.username;
        } catch (error) {
          this.userIdError = true
          this.userIdInfo = error.response.data.error;
        }
      } else {
        this.userIdError = false
        this.userIdInfo = ""
      }
    },
    async validateModelId() {
      const modelId = this.newForum.targetId;
      if (modelId) {
        try {
          const response = await api.post("/admin_sys/model", {
            model_id: modelId
          });
          this.modelIdError = false
          this.modelIdInfo = response.data.model_name;
        } catch (error) {
          this.modelIdError = true
          this.modelIdInfo = error.response.data.error;
        }
      } else {
        this.modelIdError = false
        this.modelIdInfo = ""
      }
    },

    // 提交创建论坛表单
    async createForum() {
      this.showCreateForum = false; // 成功后关闭弹窗
      try {
        // 假设这里会将表单数据提交给后端
        const response = await api.post('/forum_sys/create_post',{
          title: this.newForum.title,
          content: this.newForum.content,
          owner_id: this.currentUserId,
          target_id: this.newForum.targetId,
          target_type: this.targetType,
        });
        console.log('Forum created:', response.data);
        
        await this.loadAllForum()
        this.showCreateForum = false; // 成功后关闭弹窗
      
      } catch (error) {
        console.error('Error creating forum:', error);
      }
    },
    async loadAllForum(){
      const response = await api.post('/forum_sys/get_all_posts',{
        });
        console.log("forums",response.data)
        this.forums=[]
        response.data.forEach((item, index) => {
          this.forums.push({
            id: item.post_id,
            title: item.title,
            owner_id: item.owner_id,
            created_at: item.created_at,
            target_id: item.target_id,
            target_type: item.target_type,
            content: item.content,
            logs: [
              
            ]
          })
        });
    },
    // 创建日志
    createLog() {
      if (!this.selectedForum) {
        console.error('No forum selected!');
        return;
      }

      const newLogData = {
        post_id: this.selectedForum.id,
        sender_id: this.currentUserId,
        message: this.newLog.message,
      };

      api.post("/forum_sys/create_post_log",newLogData)
      
      this.showCreateLog=false
    },
    async loadCurrentForumLog(){
      const response = await api.post("/forum_sys/get_post_logs",{
        post_id: this.selectedForum.id
      })
      this.selectedForum.logs=response.data
    },
  },
  // mounted() {
  //   this.filteredForums = this.forums; // 初始化时展示所有论坛
  // },
};
</script>

<style scoped>

#app {
  font-family: 'Arial', sans-serif;
}

.search-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  position: relative;
  width: 100%; /* 确保容器宽度为100% */
  max-width: 600px; /* 可选：设置最大宽度，使其不超过某个宽度 */
  margin: 0 auto; /* 确保容器在父元素中水平居中 */
}

.search-select {
  margin-right: 2px; /* 下拉框和输入框之间的间距 */
  padding: 5px 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-input {
  width: 100%;
  padding: 8px 10px 8px 35px; /* 留出空间给图标 */
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.search-input::placeholder {
  color: black /* 设置占位符文本的颜色 */
}

.search-select::placeholder {
  color: black
}

.search-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* 使用 transform 来使图标完全居中 */
  width: 18px;
  height: 18px;
  z-index: 5; /* 确保图标在按钮下层 */
}

.search-button {
  position: absolute; /* 绝对定位按钮 */
  top: 0.27cm;
  right: 0.05cm;
  bottom: 0;
  left: auto;
  cursor: pointer;
  border: none;
  padding: 0;
  width: 30px; /* 适配按钮大小 */
  height: 30px; /* 适配按钮大小 */
  z-index: 10; /* 确保按钮在最上层 */
  pointer-events: auto; /* 确保按钮可以接收到点击事件 */
  border-radius: 10%;  /* 圆形按钮 */
  display: flex;
  justify-content: center;
  align-items: center;
  transition: border-color 0.3s ease, background-color 0.3s ease; /* 边框颜色和背景颜色过渡 */
}

.search-button:focus,
.search-button:active {
  border-color: #ff5733;  /* 点击或获得焦点时，边框变为橙红色 */
  outline: none;  /* 移除焦点时的默认轮廓 */
  background-color: #2a3d75;  /* 点击时背景颜色变为深蓝色 */
}

.search-button:hover {
  border-color: #0056b3;  /* 鼠标悬停时的边框颜色 */
}


.top-navbar {
  background: url("@/img/middleBG.png");
  opacity: 0.80;
  color: white;
  padding: 0.5px;
  text-align: center;
  font-size: 1.5em;
}

.top-navbar h1 {
  font-size: 60px;
  font-weight: bold;
  color: white; /* 设置文字的颜色 */
  text-shadow: -2px -2px 0px #000, /* 上左 */ 2px -2px 0px #000, /* 上右 */ -2px 2px 0px #000, /* 下左 */ 2px 2px 0px #000; /* 下右 */
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

.correct {
  color: #4c5caf;
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
  background-color: #4c5caf;
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
  background-color: #4c5caf;
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

/* 日志容器样式 */
.logs {
  margin-top: 20px;
  background-color: #f7f9fc; /* 淡蓝色背景 */
  padding: 20px;
  border-radius: 0 0 8px 8px; /* 圆角 */
  display: flex;
  flex-direction: column;
  gap: 10px; /* 增加日志项之间的间隔 */
  flex-grow: 1;
}

/* 日志项样式 */
.log-item {
  background-color: white;
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 6px; /* 圆角 */
  display: flex;
  flex-direction: column;
}

/* 日志项内容样式 */
.log-item p {
  margin: 5px 0;
}

.log-item p strong {
  color: #4c5caf; /* 角色标题的蓝色 */
}

/* 日志时间样式 */
.log-item p small {
  color: #888; /* 时间的灰色 */
}

.button-container {
  text-align: center; /* 水平居中 */
  width: 100%; /* 父容器宽度 */
  margin-top: 5px; /* 可选：调整按钮的顶部间距 */
}

/* 按钮样式 */
.btn {
  padding: 10px 10px;
  font-size: 16px;
  background-color: #4c5caf;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

/* 日志容器的顶部 */
h3 {
  font-size: 1.2em;
  margin-bottom: 10px;
}
</style>