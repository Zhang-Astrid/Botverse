<template>
  <el-container>
    <Sidebar @toggleView="switchView" />
    <el-main>
      <component :is="currentView" />
    </el-main>
  </el-container>
  <ul>
    <li><a :href="links.main" class="styled-link">返回主界面</a></li>
    <li><a :href="links.login" class="styled-link">退出登录</a></li>
  </ul>

</template>

<script>
import Sidebar from './components/Sidebar.vue';
import UserInfo from './components/UserInfo.vue'; // 假设这是你的User组件
import MyBot from './components/MyBot.vue'; // 机器人信息组件
import Messages from './components/Messages.vue';
import AdminPanel from "@/views/user/components/AdminPanel.vue";
import Notifications from "@/views/user/components/Notifications.vue";
import axios from "axios"; // 留言组件

export default {
  name: 'MainView',
  components: {
    Sidebar,
    UserInfo,
    MyBot,
    Messages,
    Notifications,
  },
  data() {
    return {
      currentView: UserInfo,
      data: 1,
      showComponents: false,
      links:{
        main:"/main",
        login:"/login"
      },
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
        case '4':
          this.currentView = AdminPanel;
          break;
        case '5':
          this.currentView = Notifications;
          break;
        default:
          this.currentView = UserInfo;
      }
    },
  },
};
</script>

<style scoped>
.styled-link {
  display: block;
  text-align: right;
  margin: 0 auto;
  width: fit-content;
  font-size: 18px;
  color: #333;
  font-family: Arial, sans-serif;
  text-decoration: none;
  border-bottom: 2px solid #4c5caf;
  padding: 10px 20px; /* 添加一些内边距 */
  transition: all 0.3s ease; /* 平滑过渡效果 */
}

.styled-link:hover {
  color: #4c5caf;
  border-bottom: 2px solid #4c5caf;
  background-color: #eee8aa;
}
</style>