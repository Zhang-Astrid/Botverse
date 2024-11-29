<template>
  <div id="bot">
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
          <InputBox @send-message="handleSendMessage" @toggleMonocycle="toggleMonocycle" @forget-message="forgetMessage"/>
        </div>
      </div>
      <div class="history">
        <h3>History</h3>
        <ul v-if="history && history.length">
          <li v-for="(item, index) in history" :key="item.id" class="history-item">
            <div class="history-content">
              <strong>{{ item.sessionName }}</strong>
              <small>({{ formatTime(item.time) }})</small>
            </div>
            <!-- 每条消息旁的按钮 -->
            <div class="history-actions">
              <button @click="sessionname(item)">Enter</button>
              <button @click="editSessionName(index)">Change Name</button>
            </div>
            <!-- 显示输入框编辑会话名称 -->
            <div v-if="item.editing" class="session-name-edit">
              <input v-model="item.newName" placeholder="Enter new session name" />
              <button @click="updateSessionName(index)">Confirm</button>
              <button @click="cancelEdit(index)">Cancel</button>
            </div>
          </li>
        </ul>
        <p v-else>No history</p>
      </div>
    </div>
  </div>
</template>

<script>
import { nextTick, reactive } from "vue";
import Sidebar from "@/views/bot/components/SideBar.vue";
import ChatBox from "@/views/bot/components/ChatBox.vue";
import InputBox from "@/views/bot/components/InputBox.vue";
import api from "@/api/api.js";

export default {
  components: { Sidebar, ChatBox, InputBox },
  data() {
    return {
      sessionId: null, // 当前会话 ID
      history: [
        {
          id: 1, // 唯一的历史记录 ID
          role: "user", // 消息的角色（如 user, bot）
          message: "Hello, how are you?", // 消息内容
          time: 1630496168000, // 消息时间戳（UNIX时间戳）
          sessionName: "My Session", // 会话名称（可选）
          newName: "", // 用于编辑会话名称时的新名称（可选）
          editing: false, // 用于表示是否正在编辑会话名称（可选）
        },
        {
          id: 2,
          role: "bot",
          message: "I'm doing well, thank you for asking!",
          time: 1630496172000,
          sessionName: "My Session",
          newName: "",
          editing: false,
        },
        // 更多历史记录...
      ], // 历史消息
      messages: [{ role: "bot", text: "Ask me anything!" }], // 当前对话消息
      sessionLimit: 4, // 初始 session_limit
      ownerId: 1,
      modelId: 1,
      sub_sessionId: 0,
    };
  },
  methods: {
    async createSession() {
      try {
        const response = await api.post("/chat_sys/create_session", {
          session_name: "My New Session",
          model_id: this.modelId,
          owner_id: this.ownerId,
        });
        this.sessionId = response.data.id;
        console.log("Session created:", this.sessionId);
      } catch (error) {
        console.error("Error creating session:", error);
      }
    },
    async handleSendMessage(message) {
      try {
        if (!this.sessionId) {
          await this.createSession();
        }

        // 添加用户消息
        this.messages.push({ role: "user", text: message });

        // 向后端发送用户消息
        await api.post("/chat_sys/create_log", {
          session_id: this.sessionId,
          role: "user",
          message: message,
        });
        let response;
        if (this.sessionLimit === 4) {
          response = await fetch("https://api.aiproxy.io/v1/chat/completions", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer sk-iiEY0IByanFKFqpERT27TwkauSK7GOrIgLKCIANsuiAiDGMI`,
            },
            body: JSON.stringify({
              model: "gpt-4o-mini",
              messages: [{ role: "user", content: message }],
              temperature: 0.7,
              session_id: this.sessionId + "_" + this.sub_sessionId,
              session_limit: this.sessionLimit,
              stream: true,
            }),
          });
        } else {
          response = await fetch("https://api.aiproxy.io/v1/chat/completions", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer sk-iiEY0IByanFKFqpERT27TwkauSK7GOrIgLKCIANsuiAiDGMI`,
            },
            body: JSON.stringify({
              model: "gpt-4o-mini",
              messages: [{ role: "user", content: message }],
              temperature: 0.7,
              stream: true,
            }),
          });
        }
        if (!response.body) {
          throw new Error("No response body.");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let botMessage = ""; // 用于存储完整的消息内容
        let done = false;

        // 添加占位符消息
        const tempMessage = reactive({ role: "bot", text: "" });
        this.messages.push(tempMessage);

        // 流式读取并逐步更新消息
        while (!done) {
          const { value, done: readerDone } = await reader.read();
          if (readerDone) break;

          if (value) {
            const chunk = decoder.decode(value, { stream: true });

            // 按行拆分数据块
            const lines = chunk.split("\n").map((line) => line.trim());

            // 处理每一行
            for (const line of lines) {
              if (!line) continue;  // 跳过空行

              if (line === "data:") continue;
              // 处理特殊的 [DONE] 标志，跳过它
              if (line === "[DONE]") {
                done = true;
                break;
              }
              try {
                // 解析数据并更新消息内容
                const parsedData = JSON.parse(line.replace(/^data:\s*/, ""));
                // 确保解析的数据包含内容
                if (parsedData.choices && parsedData.choices[0].delta.content) {
                  const newContent = parsedData.choices[0].delta.content;
                  botMessage += newContent;
                  // 实时更新占位符消息
                  tempMessage.text = botMessage;
                }
              } catch (error) {
                console.error("JSON 解析错误:", error, line);
                done = true;
              }
            }
          }
        }
        await api.post("/chat_sys/create_log", {
          session_id: this.sessionId,
          role: "bot",
          message: botMessage,
        });
        console.log("流式传输完成: ", botMessage);
      } catch (error) {
        console.error("发送消息时出错:", error);
      }
    },
    forgetMessage() {
      this.sub_sessionId = this.sub_sessionId + 1;
    },
    toggleMonocycle() {
      if (this.sessionLimit === 4) {
        this.sessionLimit = 0;
        alert("单轮模式")
      } else {
        this.sessionLimit = 4;
        alert("多轮模式")
      }
    },
    formatTime(timestamp) {
      const date = new Date(timestamp);
      return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
    },
    sessionname(item) {
      console.log(`Session clicked: ${item.message}`);
      // 在此处理会话名称的逻辑
    },
    editSessionName(index) {
      const session = this.history[index];
      session.editing = true;
    },
    updateSessionName(index) {
      const session = this.history[index];
      if (session.newName.trim()) {
        session.sessionName = session.newName;
        session.editing = false;
        session.newName = "";
        console.log(`Session name updated: ${session.sessionName}`);
      } else {
        alert("请输入有效的名称。");
      }
    },
    cancelEdit(index) {
      const session = this.history[index];
      session.editing = false;
      session.newName = "";
    },
  },
};
</script>

<style scoped>
/* 样式统一 */
* {
  padding: 0;
  margin: 0;
  border: 0;
  box-sizing: border-box;
}

html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

#app {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.main-container {
  display: flex;
  flex-grow: 1;
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
  color: #ffa500;
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

.history-actions {
  display: flex;
  flex-direction: column;
  margin-top: 10px;
}

.history-actions button {
  width: 100%;
  padding: 5px;
  margin: 5px 0;
  background-color: #333;
  color: white;
  border: none;
  cursor: pointer;
}

.history-actions button:hover {
  background-color: #444;
}

.history-item {
  display: flex;
  justify-content: space-between;
}

.history-content {
  flex: 1;
}

.session-name-edit {
  margin-top: 10px;
}

.session-name-edit input {
  padding: 5px;
  margin-right: 5px;
}

.session-name-edit button {
  padding: 5px;
  background-color: #333;
  color: white;
  border: none;
  cursor: pointer;
}

.session-name-edit button:hover {
  background-color: #444;
}

</style>
