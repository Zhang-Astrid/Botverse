<template>
  <el-card class="box-card">
    <div slot="header" class="clearfix">
      <span>管理员面板</span>
    </div>
    <el-tabs v-model="activeTab">
      <el-tab-pane label="设置自定义机器人价格" name="first">
        <CustomRobotsPrices />
      </el-tab-pane>
      <el-tab-pane label="管理默认机器人" name="second">
        <ManageDefaultRobots />
      </el-tab-pane>
      <el-tab-pane label="导出数据报告" name="third">
        <ExportDataReport />
      </el-tab-pane>
    </el-tabs>
  </el-card>
</template>

<script>
import CustomRobotsPrices from './CustomRobotsPrices.vue';
import ManageDefaultRobots from './ManageDefaultRobots.vue';
import ExportDataReport from './ExportDataReport.vue';

export default {
  name: 'AdminPanel',
  components: {
    CustomRobotsPrices,
    ManageDefaultRobots,
    ExportDataReport
  },
  data() {
    return {
      activeTab: 'first'
    };
  }
};
</script>

<style scoped>
/* 样式内容 */
</style>