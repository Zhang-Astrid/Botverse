<template>
  <section class="comments-section">
    <h2>留言区</h2>
    <div v-for="comment in comments" :key="comment.id" class="comment">
      <div class="comment-header">
        <strong>{{ comment.sender_name }}</strong>
        <span>{{ new Date(comment.created_at).toLocaleString() }}</span>
      </div>
      <p>{{ comment.content }}</p>
    </div>

    <div class="comment-form">
      <input type="text" v-model="newComment" placeholder="写下你的评论..."/>
      <button @click="submitComment">提交评论</button>
    </div>
  </section>
</template>

<script>
import api from "@/api/api.js";
import axios from "axios";

export default {
  name: 'Messages',
  data() {
    return {
      messages: [
        {author: 'User 1', content: 'Great bot!', date: '2024-01-01'},
        {author: 'User 2', content: 'Thank you!', date: '2024-01-02'},
        // 更多留言数据...
      ],
      comments: [
        {
          id: 1,
          sender_id: "用户123",
          created_at: "2024-11-29",
          content: "这是个好人",
        },

      ],
      newComment: "",
      current_userId: "",
    };
  },
  async created() {
    const current_info = await axios.post('http://127.0.0.1:8080/user_sys/acquire_current_user',
        {}
    );
    this.current_userId = current_info.data.user_id;
    await this.loadComments();
  },
  methods: {

    async submitComment() {
      if (this.newComment.trim()) {
        // alert(this.current_userId)
        // alert(this.$route.params.user_id)
        // alert(this.newComment)
        await api.post("/comment_sys/send_comment", {
          sender_id: this.current_userId,
          target_id: this.$route.params.user_id,
          target_type: "user",
          content: this.newComment,
        })
        await this.loadComments();
        this.newComment = "";
      }
    },
    async loadComments() {
      const response = await api.post("/comment_sys/get_comments", {
        target_id: this.$route.params.user_id,
        target_type: "user",
      })
      this.comments = response.data
    },
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
  color: #4c5caf;
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
  background-color: #4c5caf;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.comment-form button:hover {
  background-color: #eee8aa;
  color: #4c5caf;
}
</style>