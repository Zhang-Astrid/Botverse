<template>
  <div>
    <el-button type="primary" @click="openAddRobotDialog">添加机器人</el-button>
    <el-table :data="robots" style="width: 100%">
      <el-table-column prop="id" label="MID" ></el-table-column>
      <el-table-column prop="name" label="机器人名称" ></el-table-column>
      <el-table-column prop="type" label="类型" ></el-table-column>
      <el-table-column prop="cost" label="价格" ></el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleEdit(scope.row.id)">编辑</el-button>
          <el-button size="small" type="primary" @click="deleteRobot(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="添加机器人" v-model="dialogVisible" width="30%">
      <el-form ref="robotForm" :model="newRobot">
        <el-form-item label="名称" label-width="70px">
          <el-input v-model="newRobot.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="类型" label-width="70px">
          <el-input v-model="newRobot.type" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="价格" label-width="70px">
          <el-input v-model="newRobot.cost" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="addRobot">确认添加</el-button>
      </span>
    </el-dialog>


    <el-dialog title="修改机器人" v-model="editlogVisible" width="30%">
      <el-form ref="robotForm" :model="newRobot">
        <el-form-item label="名称" label-width="70px">
          <el-input v-model="newRobot.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="类型" label-width="70px">
          <el-input v-model="newRobot.type" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="价格" label-width="70px">
          <el-input v-model="newRobot.cost" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editlogVisible = false">取消</el-button>
        <el-button type="primary" @click="editRobot">确认修改</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: 'ManageDefaultRobots',
  data() {
    return {
      robots: [
        { name: 'Bot 1', type: 'Chat', status: 'active' },
        { name: 'Bot 2', type: 'Assistant', status: 'inactive' }
      ],
      newRobot: {
        id:0,
        name: '',
        type: '',
        cost: ''
      },
      dialogVisible: false,
      editlogVisible: false
    };
  },
  created(){
    // alert("START")
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
        // alert(response.status);
        if (response.status === 200) {

          // alert(JSON.stringify(response.data))
          this.robots=response.data

          // 跳转到其他页面或刷新
          // window.location.href = '/dashboard'; // 示例跳转
        }
      } catch (error) {
        // alert(error)
        // console(error)
        alert(error.response.data.error);
        //把数据改成旧数据
      }
    },
    openAddRobotDialog() {
      this.dialogVisible = true;
    },
    async addRobot() {
      try {
        // alert("START")
        // alert(this.getSharedData)
        const response = await axios.post('http://127.0.0.1:8080/admin_sys/add_model', {
          user_id: 0,
          model_name: this.newRobot.name,
          model_type: this.newRobot.type,
          cost: this.newRobot.cost,
        });
        // alert(response.status);
        if (response.status === 200) {

          await this.load_models();

        }
      } catch (error) {

        alert(error.response.data.error);
        //把数据改成旧数据
      }
      this.dialogVisible = false;
    },
    async editRobot() {
      try {
        // alert("START")
        // alert(this.getSharedData)
        const response = await axios.post('http://127.0.0.1:8080/admin_sys/update_model', {
          admin_user_id: 0,
          model_id: this.newRobot.id,
          new_model_name: this.newRobot.name,
          new_model_type: this.newRobot.type,
          new_cost: this.newRobot.cost,
        });
        // alert(response.status);
        if (response.status === 200) {

          this.load_models();

        }
      } catch (error) {

        alert(error.response.data.error);
        //把数据改成旧数据
      }
      this.editlogVisible=false
      
    },
    handleEdit(id) {
      this.newRobot.id=id
      this.editlogVisible=true
      // 编辑机器人的逻辑
      
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
            user_id: 0,
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
/* 样式内容 */
</style>