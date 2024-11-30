<template>
  <el-aside width="200px">
    <el-menu :default-active="activeIndex" @select="handleSelect">
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
    </el-menu>
  </el-aside>
</template>

<script>
export default {
  name: 'Sidebar',
  data() {
    return {
      activeIndex: '1',
    };
  },
  methods: {
    handleSelect(index, indexPath) {
      this.activeIndex = index;
      // 调用主组件的方法来切换视图
      this.$emit('toggleView', index);
    },
  },
};
</script>

<style scoped>
/* 侧边栏样式 */
</style>