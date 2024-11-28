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
          <!-- 传递 messages 数据给 ChatBox -->
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
      messages: [{role: "bot" ,text: "Ask me all you want~" }], // 当前聊天内容
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
        alert(JSON.stringify(response.data));
        this.sessionId = response.data.id;
        alert(this.sessionId);
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

    // 更新前端显示：添加用户消息
    this.messages.push({ role: "user", text: message });

    // 发送到后端保存日志
    const response = await api.post("/chat_sys/create_log", {
      session_id: this.sessionId, // 使用当前 session_id
      role: "user",
      message: message,
    });

    // 调用外部AI接口获取机器人回复
    const botResponse = await axios.post('https://aiproxy.io/api/v1/chat/completions', {
      model: "gpt-3.5-turbo",  // 使用适当的模型名称
      messages: [
        { role: "user", content: message }  // 传递用户消息给模型
      ]
    }, {
      headers: {
        'Authorization': `Bearer sk-iiEY0IByanFKFqpERT27TwkauSK7GOrIgLKCIANsuiAiDGMI`  // API密钥
      }
    });

    // 获取并展示机器人回复
    const botMessage = botResponse.data.choices[0].message.content;

    // 更新前端显示：添加机器人回复
    this.messages.push({
      role: "bot",
      text: botMessage, // 使用来自API的实际回复
    });

    console.log("Message sent and bot response received:", botMessage);
  } catch (error) {
    console.error("Failed to send message or fetch bot response:", error);
  }
}
,
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
