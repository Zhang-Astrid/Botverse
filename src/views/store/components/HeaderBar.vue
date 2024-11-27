<template>
  <header class="header-bar">
    <div class="logo">
      <img src="@/img/logo.png" alt="Logo" />
    </div>
    <nav>
      <ul>
        <li><a href="#">Main</a></li>
        <li><a href="#">Chat</a></li>
        <li><a href="#">Bots</a></li>
        <li><a href="#">Community</a></li>
      </ul>
    </nav>
    <input type="text" placeholder="Search..." class="search-bar" />
  </header>
</template>

<script>
export default {
  name: "HeaderBar",
};
</script>

<style scoped>

.logo img {
  height: 100%; /* 图标高度适配顶部栏 */
  max-height: 50px; /* 设置最大高度，避免图标过大 */
  width: auto; /* 保持图标宽高比 */
  object-fit: contain; /* 确保图标内容适配容器 */
}


.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0;
  background-color: #2e3b54;
  color: #fff;
}

nav ul {
  list-style: none;
  display: flex;
  gap: 20px;
  margin: 0;
  padding: 0;
}

nav ul li a {
  color: #fff;
  text-decoration: none;
  font-size: 1rem;
}

.search-bar {
  padding: 10px;
  border-radius: 4px;
  border: none;
  background-color: #1f2937;
  color: white;
}
</style>
