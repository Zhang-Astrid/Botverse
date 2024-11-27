<template>
  <div>
    <el-button type="primary" @click="exportData">导出数据报告</el-button>
  </div>
</template>

<script>
export default {
  name: 'ExportDataReport',
  methods: {
    exportData() {
      // 实现导出数据报告的逻辑
      console.log('导出数据报告');
    }
  }
};
</script>

<style scoped>
/* 样式内容 */
</style>