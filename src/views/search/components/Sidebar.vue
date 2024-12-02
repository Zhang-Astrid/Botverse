<template>
  <div class="sidebar">
    <ul>
      <li @click="navigate('search')">搜索</li>
      <li @click="navigate('ranking')">排行榜</li>
    </ul>
  </div>
</template>

<script>
export default {
  methods: {
    navigate(page) {
      this.$emit('navigate', page);
    }
  }
};
</script>

<style scoped>
.sidebar {
  width: 80px;
  background-color: #f7f7f7;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  padding: 15px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.sidebar li:hover {
  background-color: #0066cc;
  color: white;
}
</style>
