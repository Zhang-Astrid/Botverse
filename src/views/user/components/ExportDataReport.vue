<template>
  <div>
    <el-button type="primary" @click="exportData">导出数据报告</el-button>
  </div>
</template>

<script>
import axios from "axios";
import * as XLSX from "xlsx";
export default {
  name: 'ExportDataReport',
  methods: {
    async exportData() {
      const user_jsonData = await axios.post('http://127.0.0.1:8080/admin_sys/get_all_users',{});
      const model_c_jsonData = await axios.post('http://127.0.0.1:8080/admin_sys/get_all_users_model',{});
      const model_d_jsonData = await axios.post('http://127.0.0.1:8080/admin_sys/get_models_by_user', {
          user_id: 0,
        });
      user_jsonData.data.forEach(model => {
        delete model.image;
      });
      const worksheet_user = XLSX.utils.json_to_sheet(user_jsonData.data);
      const workbook_user = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(workbook_user, worksheet_user, 'Sheet1');
      XLSX.writeFile(workbook_user, 'users.xlsx');
      const worksheet_mc = XLSX.utils.json_to_sheet(model_c_jsonData.data);
      const workbook_mc = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(workbook_mc, worksheet_mc, 'Sheet1');
      XLSX.writeFile(workbook_mc, 'customize_models.xlsx');
      const worksheet_md = XLSX.utils.json_to_sheet(model_d_jsonData.data);
      const workbook_md = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(workbook_md, worksheet_md, 'Sheet1');
      XLSX.writeFile(workbook_md, 'default_models.xlsx');
    },
  }
};
</script>

<style scoped>
/* 样式内容 */
</style>