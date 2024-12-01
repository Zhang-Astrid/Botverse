<template>
  <div>
    <el-button type="primary" @click="exportData">导出数据报告</el-button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'ExportDataReport',
  methods: {
    async exportData() {
      const user_jsonData = await axios.post('http://127.0.0.1:8080/admin_sys/get_all_users'); // TODO:替换为后端导入JSON数据
      const model_c_jsonData = await axios.post('http://127.0.0.1:8080/admin_sys/get_all_users_model');
      const model_d_jsonData = await axios.post('http://127.0.0.1:8080/admin_sys/get_models_by_user', {
          user_id: 0,
        });
      //alert(JSON.stringify(jsonData.data))
      const user_jsonStr = JSON.stringify(user_jsonData.data, null, 2);
      const model_c_jsonStr = JSON.stringify(model_c_jsonData.data, null, 2);
      const model_d_jsonStr = JSON.stringify(model_d_jsonData.data, null, 2);
      let jsonStr = user_jsonStr +"\n"+ model_c_jsonStr +"\n"+ model_d_jsonStr;
      const blob = new Blob([jsonStr], {type: 'application/json'});
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
    },
  }
};
</script>

<style scoped>
/* 样式内容 */
</style>