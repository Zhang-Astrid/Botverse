<template>
  <div>
    <el-button type="primary" @click="openAddRobotDialog">添加机器人</el-button>
    <el-table :data="robots" style="width: 100%">
      <el-table-column prop="name" label="机器人名称" width="180"></el-table-column>
      <el-table-column prop="type" label="类型" width="180"></el-table-column>
      <el-table-column prop="status" label="状态" width="180"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
          <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="添加机器人" :visible.sync="dialogVisible" width="30%">
      <el-form ref="robotForm" :model="newRobot">
        <el-form-item label="名称" label-width="70px">
          <el-input v-model="newRobot.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="类型" label-width="70px">
          <el-input v-model="newRobot.type" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="状态" label-width="70px">
          <el-select v-model="newRobot.status" placeholder="请选择">
            <el-option label="激活" value="active"></el-option>
            <el-option label="禁用" value="inactive"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="addRobot">确认添加</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'ManageDefaultRobots',
  data() {
    return {
      robots: [
        { name: 'Bot 1', type: 'Chat', status: 'active' },
        { name: 'Bot 2', type: 'Assistant', status: 'inactive' }
      ],
      newRobot: {
        name: '',
        type: '',
        status: ''
      },
      dialogVisible: false
    };
  },
  methods: {
    openAddRobotDialog() {
      this.dialogVisible = true;
    },
    addRobot() {
      this.robots.push({ ...this.newRobot });
      this.dialogVisible = false;
      this.newRobot = { name: '', type: '', status: '' }; // 重置表单
    },
    handleEdit(index, row) {
      // 编辑机器人的逻辑
      console.log('编辑机器人:', index, row);
    },
    handleDelete(index, row) {
      // 删除机器人的逻辑
      console.log('删除机器人:', index, row);
      this.robots.splice(index, 1);
    }
  }
};
</script>

<style scoped>
/* 样式内容 */
</style>