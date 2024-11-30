<template>
  <div id="search" class="app-container">
    <!-- 顶部导航栏 -->
    <nav class="navbar">
      <ul>
        <li>Main</li>
        <li>Chat</li>
        <li>Bots</li>
        <li>Community</li>
        <li>Search</li>
      </ul>
    </nav>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="搜索大模型..."
        @keyup.enter="submitSearch"
      />
      <button @click="submitSearch">搜索</button>
    </div>

    <!-- 模型列表 -->
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
export default {
  data() {
    return {
      searchQuery: "",
      searchResults: [],
      models: [
        {name: "GPT-4", icon: "🤖", description: "GPT-4是最新的生成预训练模型，能够处理多种任务"},
        {name: "GPT-4O", icon: "🧠", description: "GPT-4O是针对开放问题优化的变体"},
        {name: "BERT", icon: "📝", description: "BERT用于理解语言并在文本生成中发挥作用"},
        {name: "T5", icon: "📚", description: "T5模型适用于各种文本生成任务"}
      ]
    };
  },
  methods: {
    submitSearch() {
      if (this.searchQuery.trim() === "") return;
      this.searchResults = this.models.filter(model =>
          model.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    selectModel(modelName) {
      alert(`你选择了模型: ${modelName}`);
    }
  }
};
</script>

<style scoped>
/* 整体容器 */
.app-container {
  font-family: Arial, sans-serif;
  background-color: white;
  padding: 20px;
}

/* 顶部导航栏 */
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

/* 搜索栏 */
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

/* 模型列表 */
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
