<template>
  <div class="sidebar">
    <ul>
      <li @click="navigate('search')">Search</li>
      <li @click="navigate('ranking')">Rankings</li>
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
  width: 100px;
  background-color: #57565b;
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
  color:white;
}

.sidebar li:hover {
  background-color: rgb(238, 232, 170); /* 深蓝色 */
  color: #ffffff;
  border-radius: 8px; /* 圆角 */
}
</style>
