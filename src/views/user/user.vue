<template>
  <ul class="header-links">
    <li><a :href="links.main" class="styled-link">返回主界面</a></li>
    <li><a :href="links.login" class="styled-link">退出登录</a></li>
  </ul>
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
  color: #4c5caf;
  font-family: Arial, sans-serif;
  text-decoration: none;
  padding: 10px 20px; /* 添加一些内边距 */
  transition: all 0.3s ease; /* 平滑过渡效果 */
}

.styled-link:hover {
  color: rgba(30, 41, 61, 0.56);
}

.header-links {
  display: flex;
  justify-content: flex-end; /* 让链接项靠右 */
  position: fixed; /* 固定在页面顶部 */
  top: 0;
  right: 0;
  margin: 20px; /* 距离右上角有些间隙 */
  padding: 0;
  list-style-type: none; /* 去掉默认的列表样式 */
}

.header-links li {
  margin-left: 20px; /* 给每个链接之间加点间隔 */
}
</style>