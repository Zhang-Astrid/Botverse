<template>
  <el-container>
    <Sidebar @toggleView="switchView" />
    <el-main>
      <component :is="currentView" />
    </el-main>
  </el-container>
</template>

<script>
import Sidebar from './components/Sidebar.vue';
import UserInfo from './components/UserInfo.vue'; // 假设这是你的User组件
import MyBot from './components/MyBot.vue'; // 机器人信息组件
import Messages from './components/Messages.vue'; // 留言组件

export default {
  name: 'MainView',
  components: {
    Sidebar,
    UserInfo,
    MyBot,
    Messages,
  },
  data() {
    return {
      currentView: UserInfo,
    };
  },
  methods: {
    switchView(index) {
      switch (index) {
        case '1':
          this.currentView = UserInfo;
          break;
        case '2':
          this.currentView = MyBot;
          break;
        case '3':
          this.currentView = Messages;
          break;
        default:
          this.currentView = UserInfo;
      }
    },
  },
};
</script>

<style scoped>
/* 主视图样式 */
</style>