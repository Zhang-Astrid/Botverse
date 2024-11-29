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
      const jsonData = { key: 'value' }; // TODO:替换为后端导入JSON数据
      const jsonStr = JSON.stringify(jsonData, null, 2);
      const blob = new Blob([jsonStr], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = 'data.json';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      console.log('导出数据报告');
    }
  }
};
</script>

<style scoped>
/* 样式内容 */
</style>