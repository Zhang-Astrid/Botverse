<template>
  <div id="search">
    <nav class="navbar">
      <ul>
        <li><a :href="links.main">Main</a></li>
        <li><a :href="links.chat">Chat</a></li>
        <li><a :href="links.user">User</a></li>
        <li><a :href="links.community">Community</a></li>
      </ul>
    </nav>

    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="搜索大模型..."
        @keyup.enter="submitSearch"
      />
      <button @click="submitSearch">搜索</button>
    </div>

    <!-- 添加单选框，用于选择搜索类型 -->
    <div class="search-options">
      <label>
        <input type="radio" v-model="selectedSearchType" value="model" /> 模型
      </label>
      <label>
        <input type="radio" v-model="selectedSearchType" value="user" /> 用户
      </label>
    </div>

    <div class="models-list" v-if="selectedSearchType === 'model'">
      <div v-for="(model, index) in searchResults" :key="index" class="model-card">
        <button class="model-button" @click="selectModel(model.name)">
          <div class="model-icon">{{ model.icon }}</div>
          <div class="model-name">{{ model.name }}</div>
        </button>
        <p class="model-description">{{ model.description }}</p>
      </div>
    </div>

    <!-- 可以添加用户相关的显示部分 -->
    <div class="user-list" v-if="selectedSearchType === 'user'">
      <!-- 用户列表的内容，暂时留空 -->
      <p>用户搜索功能（待实现）</p>
    </div>
  </div>
</template>

<script>
import api from "@/api/api.js";
import axios from "axios";
export default {
  props: {
    models: Array
  },
  data() {
    return {
      searchQuery: '',
      searchResults: [],
      selectedSearchType: 'model', // 默认选择模型搜索
      links: {
        main: "/main",
        chat: "/search",
        user: "/user",
        community: "/forum",
      },
    };
  },
  methods: {
    submitSearch() {
      if (this.searchQuery.trim() === '') return;
      if (this.selectedSearchType === 'model') {
        this.searchResults = this.models.filter(model =>
          model.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      } else if (this.selectedSearchType === 'user') {
        // 在这里实现用户搜索的逻辑
        // 你可以通过某个API来获取用户数据并进行筛选
        console.log('执行用户搜索: ', this.searchQuery);
      }
    },
    selectModel(modelName) {
      this.$emit('select-model', modelName);
    }
  },
  async created() {
    const response = await api.post("/user_sys/acquire_current_user", {});
    this.links.user = `/user/userId/${response.data.user_id}`;

    const response_session = await api.post("/chat_sys/get_user_sessions", {
      user_id: response.data.user_id
    });
    this.links.chat = `/chatbot/session/${response_session.data[0].id}`;
  }
};
</script>

<style scoped>
/* 搜索栏样式 */
.navbar {
  display: flex;
  justify-content: space-around;
  padding: 20px;
  background-color: white;
  color: #007bff;
  border-radius: 8px 8px 0 0;
}

.navbar ul {
  display: flex;
  list-style: none;
  gap: 20px;
}

.navbar li {
  cursor: pointer;
  transition: color 0.3s ease;
  padding: 5px 10px;
  border-radius: 4px;
}

.navbar li:hover {
  background-color: #0056b3;
  color: #ffffff;
}

.search-bar {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.search-bar input {
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.search-bar button {
  padding: 10px 20px;
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.search-bar button:hover {
  background-color: #005bb5;
}

/* 搜索类型单选框样式 */
.search-options {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.search-options label {
  font-size: 14px;
}

/* 模型卡片 */
.models-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.model-card {
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.model-button {
  background-color: #e6f0ff;
  padding: 15px;
  border-radius: 8px;
  border: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  width: 100%;
}

.model-button:hover {
  background-color: #cce0ff;
}

.model-icon {
  font-size: 30px;
}

.model-name {
  font-weight: bold;
  margin-top: 10px;
}

.model-description {
  margin-top: 10px;
  font-size: 12px;
  color: #666;
}

/* 用户列表样式 */
.user-list {
  margin-top: 20px;
  text-align: center;
}
</style>
