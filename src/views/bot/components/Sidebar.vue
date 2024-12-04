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
  width: 250px;
  background-color: #57565b;
  box-shadow: 2px 0 5px rgba(30, 41, 61, 0.56);
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  border-radius: 0px 8px 8px 8px; /* 圆角 */
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  padding: 15px;
  cursor: pointer;
  transition: background-color 0.3s;
  justify-content: center;
  height: 20px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-top: 10px;
}

.sidebar li:hover {
  background-color: rgb(144, 150, 193);

}
</style>
