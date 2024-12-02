<template>
  <div class="mybot-container">
    <el-button type="primary" @click="addRobot" v-if="is_current">创建新机器人</el-button>
    <el-table :data="robots" style="width: 100%">
      <el-table-column prop="id" label="MID"></el-table-column>
      <el-table-column prop="name" label="名称"></el-table-column>
      <el-table-column prop="type" label="类型"></el-table-column>
      <el-table-column prop="prompt" label="提示词"></el-table-column>
      <el-table-column label="操作" width="180" >
        <template #default="scope">
          <el-button @click="showDetail(scope.row.id)" type="primary" size="small">详情</el-button>
          <el-button @click="deleteRobot(scope.row.id)" type="primary" size="small" v-if="is_current">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="添加机器人" >
      <el-form ref="dataForm" :model="dataForm" label-width="100px">
        <el-form-item label="名称">
          <el-input v-model="dataForm.name"></el-input>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="dataForm.type" placeholder="请选择">
            <el-option label="gpt-3.5-turbo" value="gpt-3.5-turbo"></el-option>
            <el-option label="gpt-4o" value="gpt-4o"></el-option>
            <el-option label="gpt-4o-mini" value="gpt-4o-mini"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="提示词">
          <el-input v-model="dataForm.prompt"></el-input>
        </el-form-item>
        <el-form-item label="介绍">
          <el-input v-model="dataForm.content"></el-input>
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
      ],
      is_current: true,
      dialogVisible: false,
      dataForm: {
        name: '',
        type: '',
        prompt:'',
        content:'',
      },
      newRobot:{
        id: '',
        name:'',
        type:'',
        prompt:'',
        content:'',

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
          user_id: this.$route.params.user_id,
        });
        const current_info = await axios.post('http://127.0.0.1:8080/user_sys/acquire_current_user',
          {}
        );

        this.is_current = (+ this.$route.params.user_id === +current_info.data.user_id);
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
    showDetail(id){
      this.$router.push(`/modelview/model/${id}`).then(() => {
        window.location.reload();  // 页面跳转后刷新
      });
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
          prompt: this.dataForm.prompt,
          content: this.dataForm.content,
        });
        // alert(response.status);
        if (response.status === 200) {
          // alert(JSON.stringify(response.data))
          await this.load_models();
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

