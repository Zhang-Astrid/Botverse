<template>
  <div>
    <el-table :data="robots" style="width: 100%">
      <el-table-column prop="id" label="MID" ></el-table-column>
      <el-table-column prop="name" label="机器人名称" ></el-table-column>
      <el-table-column prop="type" label="类型" ></el-table-column>
      <el-table-column prop="cost" label="价格" ></el-table-column>
      <el-table-column prop="owner" label="创建者" ></el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleEdit(scope.row.id)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>




    <el-dialog title="修改价格" v-model="pricelogVisible" width="30%">
      <el-form ref="robotForm" :model="newRobot">
        <el-form-item label="价格" label-width="70px">
          <el-input v-model="newRobot.cost" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="pricelogVisible = false">取消</el-button>
        <el-button type="primary" @click="setPrice">确认修改</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: 'CustomRobotsPrices',
  data() {
    return {
      pricelogVisible: false,
      robots: [
        { name: 'Bot 1', type: 'Chat', status: 'active' },
        { name: 'Bot 2', type: 'Assistant', status: 'inactive' }
      ],
      newRobot:{
        id:0,
        cost:0,
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
        const response = await axios.post('http://127.0.0.1:8080/admin_sys/get_all_users_model', {
          
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
    handleEdit(id){
      this.newRobot.id=id;
      this.pricelogVisible=true;
    },
    async setPrice() {
      // 实现设置价格的逻辑
      try {
        // alert("START")
        // alert(this.getSharedData)
        const response = await axios.post('http://127.0.0.1:8080/admin_sys/update_model', {
          admin_user_id: 0,
          model_id: this.newRobot.id,
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
      this.pricelogVisible=false
    }
  }
};
</script>

<style scoped>
/* 样式内容 */
</style>