<template>
  <div id="app">
    <div class="main-container">
      <Sidebar />
      <div class="content">
        <nav class="navbar">
          <ul>
            <li>Main</li>
            <li>Chat</li>
            <li>Bots</li>
            <li>Community</li>
            <li>Search</li>
          </ul>
        </nav>
        <div class="chat-section">
          <ChatBox :messages="messages" />
          <InputBox @send-message="handleSendMessage" />
        </div>
      </div>
      <div class="history">
        <h3>History</h3>
        <ul v-if="history && history.length">
          <li v-for="item in history" :key="item.id">
            <strong>{{ item.role }}</strong>: {{ item.message }}
            <small>({{ formatTime(item.time) }})</small>
          </li>
        </ul>
        <p v-else>Loading history...</p>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from "@/views/bot/components/SideBar.vue";
import ChatBox from "@/views/bot/components/ChatBox.vue";
import InputBox from "@/views/bot/components/InputBox.vue";
import api from "@/api/api.js"; // 确保引入您的 Axios 实例

export default {
  components: { Sidebar, ChatBox, InputBox },
  data() {
    return {
      sessionId: null, // 用于保存创建的 session_id
      history: [], // 保存从后端获取的历史记录
      messages: [], // 当前聊天内容
    };
  },
  methods: {
    async createSession() {
      try {
        const response = await api.post("/chat_sys/create_session", {
          session_name: "My new session",  // 用实际的 session 名称
          model_id: 1,  // 模型 ID
          owner_id: 1 // 用户 ID
        })
        this.sessionId = response.data.session_id;
        console.log("Session created with ID:", this.sessionId);
      } catch (error) {
        console.error("Failed to create session:", error);
      }
    },
    async fetchHistory() {
      try {
        if (!this.sessionId) {
          console.warn("No session ID. Cannot fetch history.");
          return;
        }
        const response = await api.get("/chat_sys/get_logs", {
          params: { session_id: this.sessionId },
        });
        this.history = response.data;
      } catch (error) {
        console.error("Failed to fetch history:", error);
      }
    },
    async handleSendMessage(message) {
      try {
        // 如果 session 未创建，则先创建
        if (!this.sessionId) {
          await this.createSession();
        }

        // 更新前端显示
        this.messages.push({ role: "user", message });

        // 发送到后端保存日志
        const response = await api.post("/chat_sys/create_log", {
          session_id: this.sessionId, // 使用当前 session_id
          role: "user",
          message,
        });

        // 模拟机器人回复（在真实场景中这里需要根据后端返回更新）
        this.messages.push({
          role: "bot",
          message: "Bot response placeholder", // 替换为实际逻辑的回复
        });

        console.log("Message sent and saved:", response.data);
      } catch (error) {
        console.error("Failed to send message:", error);
      }
    },
    formatTime(timestamp) {
      const date = new Date(timestamp);
      return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
    },
  },
  async created() {
    // 页面加载时无需立即创建 session
    console.log("App initialized. Awaiting session creation...");
  },
};
</script>

<style scoped>
/* 与之前一致，无需更改 */
* {
  padding: 0;
  margin: 0;
  border: 0;
  box-sizing: border-box; /* 确保宽度和高度包括内边距和边框 */
}

html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
  border: 0;
  overflow: hidden;
}

#app {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  margin-top: 0;
}

.main-container {
  display: flex;
  flex-grow: 1;
  height: 100vh;
  width: 100vw;
  background-color: #1e1e2f;
}

.content {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow-y: hidden;
}

.navbar {
  display: flex;
  justify-content: space-around;
  padding: 20px;
  background-color: #1e1e2f;
}

.navbar ul {
  display: flex;
  list-style: none;
  gap: 20px;
}

.navbar li {
  color: #ffffff;
  cursor: pointer;
  transition: color 0.2s;
}

.navbar li:hover {
  color: #ffa500; /* A highlight color */
}

.chat-section {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  justify-content: space-between;
  overflow: hidden;
}

.history {
  width: 300px;
  background-color: #1e1e2f;
  padding: 20px;
  color: white;
  overflow-y: auto;
}

.history h3 {
  margin-bottom: 15px;
  font-size: 1.2rem;
}

.history ul {
  list-style: none;
  padding: 0;
}

.history li {
  margin-bottom: 10px;
  font-size: 0.9rem;
  line-height: 1.4;
}

.history small {
  color: #888;
  margin-left: 5px;
}
</style>
