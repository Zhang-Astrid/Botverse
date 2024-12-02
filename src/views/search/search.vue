<template>
  <div id="app" class="app-container">
    <!-- 左侧Sidebar -->
    <Sidebar @navigate="showPage"/>

    <!-- 右侧内容区域 -->
    <div class="content">
      <!-- 搜索页面 -->
      <Search v-if="currentPage === 'search'" :models="models" @select-model="selectModel"/>

      <!-- 排行榜页面 -->
      <Ranking v-if="currentPage === 'ranking'" :ranking-list="rankingList" @select-model="selectModel"/>
    </div>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue';
import Search from './components/Search.vue';
import Ranking from './components/Ranking.vue';

export default {
  components: {
    Sidebar,
    Search,
    Ranking
  },
  data() {
    return {
      currentPage: 'search',  // 当前页面：search 或 ranking
      models: [
        { name: 'GPT-4', icon: '🤖', description: 'GPT-4是最新的生成预训练模型，能够处理多种任务' },
        { name: 'GPT-4O', icon: '🧠', description: 'GPT-4O是针对开放问题优化的变体' },
        { name: 'BERT', icon: '📝', description: 'BERT用于理解语言并在文本生成中发挥作用' },
        { name: 'T5', icon: '📚', description: 'T5模型适用于各种文本生成任务' }
      ],
      rankingList: [
        { name: 'GPT-4', score: 98 },
        { name: 'GPT-4O', score: 94 },
        { name: 'BERT', score: 88 },
        { name: 'T5', score: 85 }
      ]
    };
  },
  methods: {
    showPage(page) {
      this.currentPage = page;
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
  display: flex;
  font-family: Arial, sans-serif;
  background-color: white;
  height: 100vh;
}

.content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
