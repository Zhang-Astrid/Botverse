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
    <div class="top-navbar">
      <h1>Search</h1>
    </div>

   <div class="search-bar">
    <!-- 类别选择按钮 -->
    <el-radio-group v-model="searchType">
      <el-radio :label="'robot'">Model</el-radio>
      <el-radio :label="'user'">User</el-radio>
    </el-radio-group>

    <!-- 搜索框 -->
    <input
      v-model="searchQuery"
      type="text"
      placeholder="Search for……"
      @keyup.enter="submitSearch"
    />
    <button @click="submitSearch">Search</button>
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
  <div>
    <!-- 表格 -->
    <el-table :data="model_info" v-if="model_info_visible" style="width: 100%">
      <el-table-column label="模型名称" width="180">
        <template #default="scope">
          <a :href="'modelview/model/' + scope.row.model_id">
            {{ scope.row.model_name }}
          </a>
        </template>
      </el-table-column>
      <el-table-column prop="model_type" label="模型类型" width="180"></el-table-column>
      <el-table-column prop="cost" label="成本"></el-table-column>
      <el-table-column prop="prompt" label="提示"></el-table-column>
      <el-table-column prop="content" label="内容"></el-table-column>
    </el-table>
    <el-table :data="user_info" v-if="user_info_visible" style="width: 100%">
      <el-table-column prop="image" label="头像">
        <template #default="scope">
          <img :src="scope.row.image" class="user-avatar" />
        </template>
      </el-table-column>
      <el-table-column prop="user_name" label="名称" width="180">
        <template #default="scope">
          <a :href="'user/userId/' + scope.row.user_id">
            {{ scope.row.user_name }}
          </a>
        </template>
      </el-table-column>
      <el-table-column prop="gender" label="性别" width="180"></el-table-column>
      <el-table-column prop="birthday" label="生日"></el-table-column>
    </el-table>
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
      model_info_visible: false,
      user_info_visible: false,
      searchType: 'robot', // 默认搜索类别为机器人
      searchQuery: '',
      model_info: [],
      user_info:[],
      links:{
        main:"/main",
        chat:"/search",
        user:"/user",
        community:"/forum",
      },
    };
  },
  methods: {
    async submitSearch() {
      if (this.searchType === 'robot') {
        this.user_info_visible = false;
        this.model_info_visible = true;
        const response = await axios.post('http://127.0.0.1:8080/search_sys/search_model',
            {hint: this.searchQuery}
        );
        this.model_info = response.data
        this.user_info = []
      }else{
        this.user_info_visible = true;
        this.model_info_visible = false;
        const response = await axios.post('http://127.0.0.1:8080/search_sys/search_user',
            {hint: this.searchQuery}
        );
        this.user_info = response.data
        this.model_info = []
      }
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
  justify-content: flex-end;
  opacity: 0.93;
  border-radius: 8px 8px 0 0; /* 圆角 */
  background: rgb(73, 72, 77);
  padding-right: 50px;
}

.navbar ul {
  display: flex;
  list-style: none;

}

.navbar li {
  cursor: pointer;
  transition: color 0.3s ease;
  padding: 5px 10px;
  border-radius: 4px;
}

.navbar li:hover {
  background-color: rgb(238, 232, 170); /* 深蓝色 */
  color: #ffffff;
}
.navbar a {
  color:white;
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
.user-avatar {
  width: 40px; /* 头像宽度 */
  height: 40px; /* 头像高度 */
  border-radius: 50%; /* 圆形头像 */
  object-fit: cover; /* 裁剪并填充 */
}

.top-navbar {
  background: url("@/img/middleBG.png");
  opacity: 0.80;
  color: white;
  padding: 0.5px;
  text-align: center;
  font-size: 1.5em;
  border-radius: 0 0 8px 8px;
}

.top-navbar h1 {
  font-size: 60px;
  font-weight: bold;
  color: white; /* 设置文字的颜色 */
  text-shadow: -2px -2px 0px #000, /* 上左 */ 2px -2px 0px #000, /* 上右 */ -2px 2px 0px #000, /* 下左 */ 2px 2px 0px #000; /* 下右 */
}
</style>
