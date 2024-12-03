<template>
  <div class="model-page">
    <header class="model-header">
      <nav class="navbar">
        <ul>
          <li><a :href="links.main">主页</a></li>
          <li><a :href="links.chat">对话</a></li>
          <li><a :href="links.user">用户</a></li>
          <li><a :href="links.community">论坛</a></li>
        </ul>
      </nav>
      <h1>{{ model.name }}</h1>
      <p class="tagline">{{ model.tagline }}</p>
      <!-- 点赞和反对按钮放置在模型详情下 -->

      <button class="enter-btn" @click="enterModel">进入模型</button>
      <div class="model-actions">
        <button @click="likeModel">👍</button>
        <button @click="dislikeModel">👎</button>
      </div>
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
          <p>{{ model.popularity }}</p>
        </div>
        <div class="stat">
          <strong>评分</strong>
          <p>👍{{ model.good_eval }}/👎{{model.bad_eval}}</p> 
        </div>
      </div>
    </section>

    <section class="comments-section">
      <h2>评论区</h2>
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
  </div>
</template>

<script>
import api from "@/api/api.js";
import axios from "axios";

export default {
  data() {
    return {
      links:{
        main:"/main",
        chat:"/chatbot/session/:sessionId",
        user:"/user/userId/:user_id",
        community:"/forum",
      },
      current_userId: 0,
      model: {
        model_id: 0,
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
          sender_id: "用户123",
          sender_name: "用户123",
          created_at: "2024-11-29",
          content: "这款模型非常智能，适用于各种应用场景，尤其在自然语言理解方面表现出色！",
        },
        {
          id: 2,
          sender_id: "小明",
          sender_name: "小明",
          created_at: "2024-11-28",
          content: "热度很高，使用体验也不错，就是积分有点贵，希望可以优化。",
        },
      ],
      newComment: "",
    };
  },
  async created() {
    this.model.model_id = this.$route.params.modelId;
    await this.loadModel();
    const response = await api.post("/user_sys/acquire_current_user",{})
    await api.post("admin_sys/eval_and_click",{
      model_id: this.model.model_id,
      add_heat:1,
    })
    this.current_userId= response.data.user_id
    await this.loadComments();
    console.log("Data", JSON.stringify(this.$data));
  },
  methods: {
    async loadComments() {
      const response = await api.post("/comment_sys/get_comments", {
        target_id: this.model.model_id,
        target_type: "model",
      });
      this.comments = response.data;
    },
    async loadModel(){
      const response=await api.post("/admin_sys/model",{
        model_id: this.model.model_id
      })
      this.model.name=response.data.model_name
      const formattedDate = new Intl.DateTimeFormat('zh-CN').format(new Date(response.data.created_at));
      this.model.tagline=`Created by ${response.data.owner_name} on ${formattedDate}`;
      this.model.description=response.data.content;
      this.model.pointsCost=response.data.cost;
      this.model.popularity=response.data.heat;
      this.model.good_eval=response.data.good_eval;
      this.model.bad_eval=response.data.bad_eval
    },
    async submitComment() {
      if (this.newComment.trim()) {
        await api.post("/comment_sys/send_comment", {
          sender_id: this.current_userId,
          target_id: this.model.model_id,
          target_type: "model",
          content: this.newComment,
        });

        await this.loadComments();
        this.newComment = "";
      }
    },
    async enterModel() {
      const response = await api.post("/chat_sys/create_session", {
        session_name: "New Session",
        model_id: this.model.model_id,
        owner_id: this.current_userId,
      });
      this.$router.push(`/chatbot/session/${response.data.id}`).then(() => {
        window.location.reload();  // 页面跳转后刷新
      });
    },

    // 点赞功能
    async likeModel() {
      await api.post("/admin_sys/eval_and_click", {
        model_id: this.model.model_id,
        add_good_eval:1
      });
      this.loadModel()
      console.log(`模型 ${this.model.model_id} 被点赞`);
    },

    // 反对功能
    async dislikeModel() {
      await api.post("/admin_sys/eval_and_click", {
        model_id: this.model.model_id,
        add_bad_eval:1
      });
      this.loadModel()
      console.log(`模型 ${this.model.model_id} 被反对`);
    },
  },
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: flex-end;
  border-radius: 8px 8px 0 0; /* 圆角 */
  background: rgb(28, 27, 33);
  padding-right: 50px;
}

.navbar ul {
  display: flex;
  list-style: none;

}

.navbar li {
  cursor: pointer;
  transition: color 0.3s ease;
  padding: 5px 10px;
  border-radius: 4px;
}

.navbar li:hover {
  background-color: rgb(76, 92, 175); /* 深蓝色 */
  color: #ffffff;
}
.navbar a {
  color:white;
}

.model-page {
  font-family: Arial, sans-serif;
  margin: 20px;
  background-color: #ffffff;
  color: #ffffff;
}

.model-header {
  background: url("@/img/middleBG.png");
  text-align: center;
  margin-bottom: 20px;
  padding-bottom: 20px;
}


.model-header h1 {
  padding-top: 60px;
  font-weight: bold;
  color: white; /* 设置文字的颜色 */
  text-shadow: -2px -2px 0px #000, /* 上左 */ 2px -2px 0px #000, /* 上右 */ -2px 2px 0px #000, /* 下左 */ 2px 2px 0px #000; /* 下右 */
  font-size: 60px;
}

.model-header .tagline {
  color: white; /* 设置文字的颜色 */
  text-shadow: -2px -2px 0px #000, /* 上左 */ 2px -2px 0px #000, /* 上右 */ -2px 2px 0px #000, /* 下左 */ 2px 2px 0px #000; /* 下右 */
  font-size: 30px;
}

.enter-btn {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 24px;
  background-color: #4c5caf;
  color: white;
  border: #000000;
  border-radius: 8px;
  cursor: pointer;
}

.enter-btn:hover {
  background-color: #eee8aa;
  color: #4c5caf;
  border-color: #000000;
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
  color: #4c5caf;
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
  color: #4c5caf;
}

.stat p {
  font-size: 18px;
  color: #444;
}

/* 模型点赞与反对按钮样式 */
.model-actions {
  display: flex;
  justify-content: space-evenly;
  margin-top: 10px;
}

.model-actions button {
  background-color: #4c5caf;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 17px;
}

.model-actions button:hover {
  background-color: #eee8aa;
  border-color: #000000;
}

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
