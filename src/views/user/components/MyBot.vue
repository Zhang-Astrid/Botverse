<template>
  <div class="mybot-container">
    <el-button type="primary" @click="createRobot">创建新机器人</el-button>
    <el-table :data="robots" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="180"></el-table-column>
      <el-table-column prop="name" label="名称"></el-table-column>
      <el-table-column prop="type" label="类型"></el-table-column>
      <el-table-column prop="status" label="状态"></el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button @click="editRobot(scope.row)" type="text" size="small">编辑</el-button>
          <el-button @click="deleteRobot(scope.row.id)" type="text" size="small">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      robots: [
        { id: 1, name: 'Robot A', type: '服务型', status: '在线' },
        { id: 2, name: 'Robot B', type: '工业型', status: '离线' },
      ],
      loading: false // 添加一个loading状态，防止表格加载时的闪烁
    };
  },
  methods: {
    createRobot() {
      this.loading = true; // 创建机器人时显示加载动画
      this.$prompt('请输入新机器人的名称', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputValidator: (value) => {
          if (!value) {
            return '名称不能为空';
          }
          return true;
        },
        inputErrorMessage: '无效的名称'
      }).then(({ value }) => {
        const newId = this.robots.length + 1;
        this.robots.push({ id: newId, name: value, type: '服务型', status: '在线' });
        this.loading = false; // 创建成功后关闭加载动画
      }).catch(() => {
        this.loading = false; // 取消操作后关闭加载动画
        this.$message({
          type: 'info',
          message: '取消输入'
        });
      });
    },
    editRobot(robot) {
      this.$prompt('编辑机器人名称', '提示', {
        value: robot.name,
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputValidator: (value) => {
          if (!value) {
            return '名称不能为空';
          }
          return true;
        },
        inputErrorMessage: '无效的名称'
      }).then(({value}) => {
        robot.name = value;
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消编辑'
        });
      });
    },
    deleteRobot(id) {
      this.$confirm('此操作将永久删除该机器人, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.robots = this.robots.filter(robot => robot.id !== id);
        this.$message({
          type: 'success',
          message: '删除成功!'
        });
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