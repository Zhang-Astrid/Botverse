<template>
  <div id="ranking">
    <nav class="navbar">
      <ul>
        <li><a :href="links.main">Main</a></li>
        <li><a :href="links.chat">Chat</a></li>
        <li><a :href="links.user">User</a></li>
        <li><a :href="links.community">Community</a></li>
      </ul>
    </nav>
    <div class="top-navbar">
      <h1>Rankings for LLM</h1>
    </div>
<!--    <h2>大模型排行榜</h2>-->
    <div class="ranking-list">
      <div v-for="(model, index) in rankingList" :key="index" class="rank-card">
        <div class="rank-position">{{ index + 1 }}</div>
        <div class="rank-info">
          <div class="rank-name">
            <a :href="'/modelview/model/'+model.id">{{ model.name }}</a>
          </div>
          <div class="rank-score">{{ model.heat }}</div>
          <!-- <div>{{ new Intl.DateTimeFormat('zh-CN').format(new Date(model.created_at))}}</div> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api/api.js";
import axios from "axios";
export default {
  props: {
    rankingList: Array
  },
  data(){
    return{
      key: "heat", //排序的关键字 "heat" "created_at" "good_eval"
      rankingList:[],
      links:{
        main:"/main",
        chat:"/search",
        user:"/user",
        community:"/forum",
      },
    }
  },
  methods: {
    enterModel(modelId) {
      this.$emit('select-model', modelId); // 触发父组件的事件，传递选择的模型名
    }
  },
  async created(){
    const response= await api.post("/user_sys/acquire_current_user",{})
    this.links.user=`/user/userId/${response.data.user_id}`
    
    const response_session= await api.post("/chat_sys/get_user_sessions",{
      user_id: response.data.user_id
    })
    this.links.chat=`/chatbot/session/${response_session.data[0].id}`
    const response_model=await api.post("/admin_sys/get_all_users_model",{
      key:this.key,
    })
    console.log(JSON.stringify(response_model.data))
    this.rankingList=response_model.data
    console.log(this.rankingList)
  }
};
</script>

<style scoped>
/* 排行榜样式 */
.navbar {
  display: flex;
  justify-content: flex-end;
  opacity: 0.93;
  border-radius: 8px 8px 0 0; /* 圆角 */
  background: rgb(73, 72, 77);
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
  background-color: rgb(238, 232, 170); /* 深蓝色 */
  color: #ffffff;
}

.navbar a {
  color: white;
}

.ranking-list {
  padding-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.rank-card {
  display: flex;
  align-items: center;
  justify-content: space-between; /* 添加空间分隔 */
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.rank-position {
  font-size: 18px;
  font-weight: bold;
  margin-right: 15px;
}

.rank-info {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.rank-name {
  font-weight: bold;
}

.rank-score {
  color: #007bff;
}

/* 进入按钮样式 */
.enter-button {
  padding: 8px 15px;
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 10px;
  margin-right: 10px; /* 保留按钮后的间距，相当于两个空格 */
}

.enter-button:hover {
  background-color: #005bb5;
}
.top-navbar {
  background: url("@/img/middleBG.png");
  opacity: 0.80;
  color: white;
  padding: 0.5px;
  text-align: center;
  font-size: 1.5em;
  border-radius: 0 0 8px 8px;
}

.top-navbar h1 {
  font-size: 60px;
  font-weight: bold;
  color: white; /* 设置文字的颜色 */
  text-shadow: -2px -2px 0px #000, /* 上左 */ 2px -2px 0px #000, /* 上右 */ -2px 2px 0px #000, /* 下左 */ 2px 2px 0px #000; /* 下右 */
}
</style>
