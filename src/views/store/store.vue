<template>
  <div id="store">
    <HeaderBar />
    <DashBoard />  <!-- 直接渲染Dashboard组件 -->
  </div>
</template>

<script>
import HeaderBar from "@/views/store/components/HeaderBar.vue";
import DashBoard from "@/views/store/components/DashBoard.vue";  // 引入Dashboard组件

export default {
  name: "App",
  components: {
    HeaderBar,
    DashBoard,  // 注册Dashboard组件
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
  background-color: #1f2937;
  height: 100vh;
}
</style>
