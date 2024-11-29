<template>
  <div class="mybot-container">
    <el-button type="primary" @click="addRobot">创建新机器人</el-button>
    <el-table :data="robots" style="width: 100%" v-loading="loading">
      <el-table-column prop="name" label="名称"></el-table-column>
      <el-table-column prop="type" label="类型"></el-table-column>

      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button @click="deleteRobot(scope.row.id)" type="primary" size="small">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="添加机器人">
      <el-form ref="dataForm" :model="dataForm" label-width="100px">
        <el-form-item label="名称">
          <el-input v-model="dataForm.name"></el-input>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="dataForm.type" placeholder="请选择">
            <el-option label="A" value="A"></el-option>
            <el-option label="B" value="B"></el-option>
            <el-option label="C" value="C"></el-option>
            <el-option label="D" value="D"></el-option>
            <el-option label="E" value="E"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>

import UserInfo from "@/views/user/components/UserInfo.vue";
import axios from "axios";
import { mapGetters } from 'vuex';
export default {
  computed: {
    ...mapGetters(['getSharedData']),
  },
  data() {
    return {
      robots: [
        { id: 1, name: 'Robot A', type: 'A' },
        { id: 2, name: 'Robot B', type: 'B' },
      ],
      loading: false,
      dialogVisible: false,
      dataForm: {
        name: '',
        type: ''
      },
      newRobot:{
        id: 1,
        name:'',
        type:'',

      }
    };
  },
  created(){
    this.load_models();
  },
  methods: {
    async load_models(){
      try {
        // alert("START")
        // alert(this.getSharedData)
        const response = await axios.post('http://127.0.0.1:8080/admin_sys/get_models_by_user', {
          user_id: this.getSharedData,
        });
        // alert(response.status);
        if (response.status === 200) {

          // alert(JSON.stringify(response.data))
          this.robots=response.data

          // 跳转到其他页面或刷新
          // window.location.href = '/dashboard'; // 示例跳转
        }
      } catch (error) {

        alert(error.response.data.error);
        //把数据改成旧数据
      }
    },
    addRobot() {
      this.dialogVisible = true;
    },
    async submitForm() {
      try {
        // alert("START")
        // alert(this.getSharedData)
        const response = await axios.post('http://127.0.0.1:8080/admin_sys/add_model', {
          user_id: this.getSharedData,
          model_name: this.dataForm.name,
          model_type: this.dataForm.type,
        });
        // alert(response.status);
        if (response.status === 200) {

          // alert(JSON.stringify(response.data))
          this.load_models();
          

          // 跳转到其他页面或刷新
          // window.location.href = '/dashboard'; // 示例跳转
        }
      } catch (error) {

        alert(error.response.data.error);
        //把数据改成旧数据
      }
      this.dialogVisible = false;
    },
    deleteRobot(id) {
      this.$confirm('此操作将永久删除该机器人, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          // alert("START")
          // alert(this.getSharedData)
          const response = await axios.post('http://127.0.0.1:8080/admin_sys/delete_model', {
            user_id: this.getSharedData,
            model_id: id,
          });
          // alert(response.status);
          if (response.status === 200) {
            // alert(response.data.message)
            this.dialogVisible = false;
            this.load_models();
            // 跳转到其他页面或刷新
            // window.location.href = '/dashboard'; // 示例跳转
          }
        } catch (error) {

          alert(error.response.data.error);
          //把数据改成旧数据
        }
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });
    }
  }
};
</script>

<style scoped>
.mybot-container {
  margin: 20px;
}

.el-button {
  margin-bottom: 10px; /* 给按钮添加一些底部间距 */
}
</style>

