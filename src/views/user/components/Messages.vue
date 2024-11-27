<template>
  <el-card class="box-card">
    <div slot="header" class="clearfix">
      <span>留言</span>
    </div>
    <el-table :data="messages" style="width: 100%">
      <el-table-column prop="author" label="作者" width="180"></el-table-column>
      <el-table-column prop="content" label="内容"></el-table-column>
      <el-table-column prop="date" label="日期" width="180"></el-table-column>
    </el-table>
  </el-card>
</template>

<script>
export default {
  name: 'Messages',
  data() {
    return {
      messages: [
        { author: 'User 1', content: 'Great bot!', date: '2024-01-01' },
        { author: 'User 2', content: 'Thank you!', date: '2024-01-02' },
        // 更多留言数据...
      ]
    };
  }
};
</script>

<style scoped>
/* 样式内容 */
</style>