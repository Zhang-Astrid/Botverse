<template>
  <div class="model-page">
    <header class="model-header">
      <h1>{{ model.name }}</h1>
      <p class="tagline">{{ model.tagline }}</p>
      <button class="enter-btn" @click="enterModel">进入模型</button>
    </header>

    <section class="model-details">
      <div class="model-info">
        <h2>模型简介</h2>
        <p>{{ model.description }}</p>
      </div>

      <div class="model-stats">
        <div class="stat">
          <strong>消耗积分(每字符)</strong>
          <p>{{ model.pointsCost }} 积分</p>
        </div>
        <div class="stat">
          <strong>热度</strong>
          <p>{{ model.popularity }}%</p>
        </div>
        <div class="stat">
          <strong>评分</strong>
          <p>{{ model.rating }} / 5</p>
        </div>
      </div>
    </section>

    <section class="comments-section">
      <h2>评论区</h2>
      <div v-for="comment in comments" :key="comment.id" class="comment">
        <div class="comment-header">
          <strong>{{ comment.user }}</strong>
          <span>{{ comment.date }}</span>
        </div>
        <p>{{ comment.text }}</p>
      </div>

      <div class="comment-form">
        <input type="text" v-model="newComment" placeholder="写下你的评论..."/>
        <button @click="submitComment">提交评论</button>
      </div>
    </section>
  </div>
</template>

<script>
import api from "@/api/api.js";
import axios from "axios";


export default {
  data() {
    return {
      current_userId:0,
      model: {
        model_id:0,
        name: "GPT-4 O",
        tagline: "下一代智能对话系统",
        description: "GPT-4 O 是一个强大的自然语言处理模型，具有更强的理解和生成能力，广泛应用于聊天、问答、翻译等领域。",
        pointsCost: 50,
        popularity: 95,
        rating: 4.7,
      },
      comments: [
        {
          id: 1,
          user: "用户123",
          date: "2024-11-29",
          text: "这款模型非常智能，适用于各种应用场景，尤其在自然语言理解方面表现出色！",
        },
        {
          id: 2,
          user: "小明",
          date: "2024-11-28",
          text: "热度很高，使用体验也不错，就是积分有点贵，希望可以优化。",
        },
      ],
      newComment: "",
    };
  },
 async created(){
    this.model.model_id=this.$route.params.modelId;
    await this.loadModel();
    const response = await api.post("/user_sys/acquire_current_user",{})
    this.current_userId= response.data.user_id
    console.log("Data",JSON.stringify(this.$data))
  },
  methods: {
    async loadModel(){
      const response=await api.post("/admin_sys/model",{
        model_id: this.model.model_id
      })
      this.model.name=response.data.model_name
      this.model.tagline="Created by "+response.data.owner_name;
      this.model.description=response.data.content;
      this.model.pointsCost=response.data.cost;

    },
    submitComment() {
      if (this.newComment.trim()) {
        this.comments.push({
          id: this.comments.length + 1,
          user: "匿名用户",
          date: new Date().toLocaleDateString(),
          text: this.newComment,
        });
        this.newComment = "";
      }
    },
    async enterModel() {
      const response = await api.post("/chat_sys/create_session",{
        session_name: "New Session",
        model_id: this.model.model_id,
        owner_id: this.current_userId,
      })
      this.$router.push(`/chatbot/session/${response.data.id}`).then(() => {
        window.location.reload();  // 页面跳转后刷新
      });
      // 模拟进入模型的操作
      // alert("你已进入模型！");
    },
  },
};
</script>

<style scoped>
.model-page {
  font-family: Arial, sans-serif;
  margin: 20px;
  background-color: #ffffff;
  color: #333;
}

.model-header {
  text-align: center;
  margin-bottom: 20px;
}

.model-header h1 {
  font-size: 36px;
  color: #007bff;
}

.model-header .tagline {
  font-size: 18px;
  color: #555;
}

.enter-btn {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.enter-btn:hover {
  background-color: #0056b3;
}

.model-details {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 40px;
}

.model-info {
  background-color: #f0f8ff;
  padding: 15px;
  border-radius: 8px;
}

.model-info h2 {
  font-size: 24px;
  color: #007bff;
}

.model-info p {
  font-size: 16px;
  color: #555;
}

.model-stats {
  display: flex;
  justify-content: space-between;
}

.stat {
  background-color: #e6f7ff;
  padding: 15px;
  border-radius: 8px;
  width: 30%;
  text-align: center;
}

.stat strong {
  font-size: 16px;
  color: #007bff;
}

.stat p {
  font-size: 18px;
  color: #444;
}

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
