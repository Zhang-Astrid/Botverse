<template>
  <el-table :data="comments" style="width: 100%">
      <el-table-column prop="is_read" label="是否已读">
        <template #default="scope">
        <!-- 根据is_read的值来改变样式 -->
        <div :style="{ color: scope.row.is_read ? 'gray' : 'red' }">
          {{ scope.row.is_read ? '已读' : '未读' }}
        </div>
        </template>
      </el-table-column>

      <el-table-column prop="created_at" label="时间"></el-table-column>
      <el-table-column prop="information" label="通知"></el-table-column>
      <el-table-column label="操作" width="180" >
        <template #default="scope">
          <el-button @click="readComment(scope.row.id)" type="primary" size="small">详情</el-button>
        </template>
      </el-table-column>
    </el-table>

  <el-dialog v-model="dialogVisible" title="具体内容" >
      <p>{{ current_content }}</p>
      <span slot="footer" class="dialog-footer">
        <el-button @click="closeDialog">确定</el-button>
      </span>
  </el-dialog>
</template>

<script>
import api from "@/api/api.js";
import axios from "axios";

export default {
  name: 'Notifications',
  data() {
    return {
      dialogVisible: false,
      comments: [
      ],
      newComment: "",
      current_userId:"",
      current_content:"",
    };
  },
  async created() {
    await this.loadNotifications();
  },
  methods:{
    async readComment(id) {
      await api.post("/comment_sys/read_comments", {
        id:id
      })
      this.dialogVisible = true;
      this.current_content = this.comments.find(comment => comment.id === id)?.content;
    },
    async closeDialog(){
      this.dialogVisible = false;
      await this.loadNotifications();
    },
    async loadNotifications(){
      const response=await api.post("/comment_sys/get_comments_by_all_user",{
        user_id: this.$route.params.user_id,
      })
      //alert(JSON.stringify(response.data));
      this.comments=this.processComments(response.data)
    },
    processComments(data) {
      return data.map(item => {
        let information;
        if (item.model_name!== "") {
        // 如果model_name不为空，则使用新的格式
        information = `用户 ${item.sender_name} 对你的机器人 ${item.model_name} 发表了评论`;
        } else {
        // 如果model_name为空，则使用原来的格式
        information = `用户 ${item.sender_name} 对你发表了评论`;
        }
        return {
          id: item.id,
          is_read: item.has_read,
          created_at: item.created_at,
          information: information,
          content: item.content,
        };
      });
    }
  }
};
</script>

<style scoped>
.comments-section {
  background-color: #f0f8ff;
  padding: 20px;
  border-radius: 8px;
}

.comments-section h2 {
  font-size: 24px;
  color: #007bff;
  margin-bottom: 15px;
}

.comment {
  background-color: #ffffff;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #666;
}

.comment-header strong {
  color: #333;
}

.comment-form {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.comment-form input {
  flex: 1;
  padding: 10px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.comment-form button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.comment-form button:hover {
  background-color: #0056b3;
}
</style>