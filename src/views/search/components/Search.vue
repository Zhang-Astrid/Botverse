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

    <div class="models-list">
      <div v-for="(model, index) in searchResults" :key="index" class="model-card">
        <button class="model-button" @click="selectModel(model.name)">
          <div class="model-icon">{{ model.icon }}</div>
          <div class="model-name">{{ model.name }}</div>
        </button>
        <p class="model-description">{{ model.description }}</p>
      </div>
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
      links:{
        main:"/main",
        chat:"/search",
        user:"/user",
        community:"/forum",
      },
    };
  },
  methods: {
    submitSearch() {
      if (this.searchQuery.trim() === '') return;
      this.searchResults = this.models.filter(model =>
        model.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    selectModel(modelName) {
      this.$emit('select-model', modelName);
    }
  },
  async created(){
    const response= await api.post("/user_sys/acquire_current_user",{})
    this.links.user=`/user/userId/${response.data.user_id}`
    
    const response_session= await api.post("/chat_sys/get_user_sessions",{
      user_id: response.data.user_id
    })
    this.links.chat=`/chatbot/session/${response_session.data[0].id}`
  }
};
</script>

<style scoped>
/* 搜索栏样式 */
.navbar {
  display: flex;
  justify-content: space-around;
  padding: 20px;
  background-color: white; /* 蓝色背景 */
  color: #007bff;
  border-radius: 8px 8px 0 0; /* 圆角 */
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
  background-color: #0056b3; /* 深蓝色 */
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
</style>
