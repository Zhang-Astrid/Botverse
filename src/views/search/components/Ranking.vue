<template>
  <div id="ranking">
    <nav class="navbar">
      <ul>
        <li>Main</li>
        <li>Chat</li>
        <li>Bots</li>
        <li>Community</li>
        <li>Search</li>
      </ul>
    </nav>
    <h2>大模型排行榜</h2>
    <div class="ranking-list">
      <div v-for="(model, index) in rankingList" :key="index" class="rank-card">
        <div class="rank-position">{{ index + 1 }}</div>
        <div class="rank-info">
          <div class="rank-name">{{ model.name }}</div>
          <div class="rank-score">{{ model.score }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    rankingList: Array
  }
};
</script>

<style scoped>
/* 排行榜样式 */
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

.ranking-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.rank-card {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.rank-position {
  font-size: 18px;
  font-weight: bold;
  margin-right: 15px;
}

.rank-info {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.rank-name {
  font-weight: bold;
}

.rank-score {
  color: #007bff;
}
</style>
