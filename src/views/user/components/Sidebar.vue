<template>
  <el-aside class="sidebar">
    <el-menu :default-active="activeIndex" @select="handleSelect" class="sidebar_container">
      <el-menu-item index="1">
        <i class="el-icon-user"></i>
        <span>个人信息</span>
      </el-menu-item>
      <el-menu-item index="2">
        <i class="el-icon-s-promotion"></i>
        <span>用户机器人</span>
      </el-menu-item>
      <el-menu-item index="3">
        <i class="el-icon-chat-line-round"></i>
        <span>留言</span>
      </el-menu-item>
      <el-menu-item index="4" v-if="is_admin && is_current">
        <i class="el-icon-setting"></i>
        <span>管理员面板</span>
      </el-menu-item>
      <el-menu-item index="5" v-if="is_current">
        <i class="el-icon-setting"></i>
        <span>通知</span>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<script>
import axios from "axios";

export default {
  name: 'Sidebar',
  data() {
    return {
      is_admin: false,
      is_current: true,
      activeIndex: '1',
    };
  },
  created() {
    this.checkCurrent();
    this.checkAdmin()
  },
  methods: {
    async checkCurrent() {
      const current_info = await axios.post('http://127.0.0.1:8080/user_sys/acquire_current_user',
          {}
      );
      this.is_current = (+this.$route.params.user_id === +current_info.data.user_id);
    },
    async handleSelect(index) {
      this.activeIndex = index;
      this.$emit('toggleView', index);
    },
    async checkAdmin() {
      const current_info = await axios.post('http://127.0.0.1:8080/user_sys/is_admin',
          {user_id: this.$route.params.user_id}
      );
      this.is_admin = current_info.data.isAdmin;
    },
  },
};
</script>

<style scoped>
/* 侧边栏样式 */
/* Sidebar */
.sidebar {
  width: 200px;
  background: url("@/img/mainBG.png");
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 5px 20px 0;
}

.sidebar_container {
  background-color: #4c5caf;
  border-radius: 10px;
  border: 4px #eee8aa;
}



.sidebar_container:hover {
  border: 4px #4c5caf;
}

.sidebar_container span {
  color: white;
  align-items: center;
  font-size: 1.2rem;
  justify-content: center;
}


.sidebar_container span:hover {
  color: #000000;
}
</style>