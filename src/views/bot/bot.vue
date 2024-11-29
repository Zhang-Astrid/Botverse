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
          <InputBox @send-message="handleSendMessage" @toggleMonocycle="toggleMonocycle"
            @forget-message="forgetMessage" />
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
import { reactive } from "vue";
import Sidebar from "@/views/bot/components/SideBar.vue";
import ChatBox from "@/views/bot/components/ChatBox.vue";
import InputBox from "@/views/bot/components/InputBox.vue";
import api from "@/api/api.js";
import axios from "axios";
import { mapActions, mapGetters } from 'vuex';
import { timePanelSharedProps } from "element-plus/es/components/time-picker/src/props/shared";

export default {
  components: { Sidebar, ChatBox, InputBox },
  computed: {
    ...mapGetters(['getSharedData']),
    ...mapGetters(['getShared']),
  },
  data() {
    return {
      sessionId: 2, // 当前会话 ID
      history: [], // 历史消息
      messages: [{ role: "bot", text: "Ask me anything!" }], // 当前对话消息
      sessionLimit: 4, // 初始 session_limit
      ownerId: 1,
      modelId: 2,
      sub_sessionId: 0,
      session_info: {
        cost: 5,
        created_at: "Fri, 29 Nov 2024 20:29:15 GMT",
        id: 2,
        model_id: 2,
        model_name: "3",
        model_type: "4",
        owner_id: 2,
        owner_name: "testuser",
        owner_score: 0,
        session_name: "My New Session",
        sub_id: 0
      },
    };
  },
  async created() {
    this.sessionId = this.$route.params.sessionId
    this.getSessionData();
    await this.loadMessages();
    await this.loadHistory();
    // this.ownerId=this.getSharedData;

  },
  methods: {
    async loadHistory() {
      const history_info = await api.post("/chat_sys/get_user_sessions", {
        user_id: this.session_info.owner_id
      })
      let his = []
      history_info.data.forEach(function (item) {
        his.push(
          {
            id: item.id,
            sessionName: item.session_name,
            time: item.created_at, // 以 ISO 字符串格式表示时间
            editing: false,  // 是否在编辑状态
            newName: '' // 用于保存新的会话名称
          }
        )
      });
      this.history = his
      console.log("历史会话信息", JSON.stringify(this.history))
    },
    async loadMessages() {
      const msg_info = await axios.post('http://127.0.0.1:8080/chat_sys/get_logs',
        { session_id: this.sessionId }
      );
      this.messages = msg_info.data
    },
    async getSessionData() {
      const session_info = await axios.post('http://127.0.0.1:8080/chat_sys/get_session',
        { session_id: this.sessionId }
      );
      /*
      {"cost":5,"created_at":"Fri, 29 Nov 2024 20:29:15 GMT","id":2,"model_id":2,"model_name":"3","model_type":"4","owner_id":2,"owner_name":"testuser","owner_score":0,"session_name":"My New Session","sub_id":0}
      */
      console.log(JSON.stringify(session_info.data))
      // alert(JSON.stringify(new_info.data))
      this.session_info = session_info.data;
      this.sub_sessionId = this.session_info.sub_id
      // alert(new_info.data.user_id);
      this.$store.commit('updateSharedData', {
        userid: this.session_info.owner_id,
        username: this.session_info.owner_name,
        score: this.session_info.owner_score,
        model_name: this.session_info.model_name,
        session_id: this.sessionId,
        model_type: this.session_info.model_type,
      });
      console.log("Shared Data", JSON.stringify(this.getShared))
    },
    async createSession() {
      alert("create session");
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
      if (this.session_info.owner_score <= 0) {
        alert("积分不够，请充值！")
        return;
      }
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
              model: this.session_info.model_type,
              messages: [{ role: "user", content: message }],
              temperature: 0.7,
              session_id: this.sessionId + "_" + this.sub_sessionId,
              session_limit: this.sessionLimit,
              stream: true,
            }),
          });
        }
        else {
          response = await fetch("https://api.aiproxy.io/v1/chat/completions", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer sk-iiEY0IByanFKFqpERT27TwkauSK7GOrIgLKCIANsuiAiDGMI`,
            },
            body: JSON.stringify({
              model: this.session_info.model_type,
              messages: [{ role: "user", content: message }],
              temperature: 0.7,
              stream: true,
              stream_options: {"include_usage": true}
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

        let tot_tokens = 0;
        // 流式读取并逐步更新消息
        while (!done) {
          const { value, done: readerDone } = await reader.read();
          if (readerDone) break;

          if (value) {
            const chunk = decoder.decode(value, {stream: true});

            // 按行拆分数据块
            const lines = chunk.split("\n").map((line) => line.trim());

            // 处理每一行
            for (const line of lines) {
              if (!line) continue;  // 跳过空行

              if (line === "data:") continue;
              // 处理特殊的 [DONE] 标志，跳过它
              if (line === "data: [DONE]") {
                done = true;
                break;
              }
              try {
                tot_tokens = tot_tokens + 1;
                // 解析数据并更新消息内容
                const parsedData = JSON.parse(line.replace(/^data:\s*/, ""));
                // 确保解析的数据包含内容
                // console.log(parsedData);
                if (parsedData.choices && parsedData.choices[0].delta.content) {
                  const newContent = parsedData.choices[0].delta.content;
                  botMessage += newContent;
                  totalTokens++
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

        // 在消息后附加 total_tokens
        tempMessage.text += ` (Total tokens used: ${totalTokens})`;

        // 发送 bot 消息
        await api.post("/chat_sys/create_log", {
          session_id: this.sessionId,
          role: "bot",
          message: botMessage,
        });
        const modify_score = await api.post("/store_sys/update", {
          username: this.session_info.owner_name,
          increament: -tot_tokens * this.session_info.cost
        })
        console.log("剩余积分: ", modify_score.data.score)
        this.session_info.owner_score = modify_score.data.score
        await api.post("/chat_sys/update_session", {
          session_id: this.sessionId
        })
        await this.loadHistory();
        console.log("流式传输完成: ", botMessage);
      } catch (error) {
        console.error("发送消息时出错:", error);
      }
    },
    async forgetMessage() {
      this.sub_sessionId = this.sub_sessionId + 1;
      await api.post("/chat_sys/update_session", {
        session_id: this.sessionId,
        sub_id: this.sub_sessionId
      })
      const msg_info = await axios.post('http://127.0.0.1:8080/chat_sys/delete_logs',
        { session_id: this.sessionId }
      );
      await this.loadHistory();
      await this.loadMessages();
    },
    toggleMonocycle() {
      console.log("seid " + this.sessionId)
      if (this.sessionLimit === 4) {
        this.sessionLimit = 0;
        alert("单轮模式")
      }
      else {
        // 切换 session_limit 的值
        this.sessionLimit = 4;
        alert("多轮模式");
      }
    },
    formatTime(timestamp) {
      const date = new Date(timestamp);
      const formatter = new Intl.DateTimeFormat('en-US', {
        timeZone: 'Asia/Shanghai', // 或者 'UTC' 或 'Asia/Shanghai'
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      });
      return formatter.format(date);
    },
    sessionname(item) {
      console.log(`Session clicked: ${item.message}`);
    },
    editSessionName(index) {
      const session = this.history[index];
      session.editing = true;
    },
    async updateSessionName(index) {
      const session = this.history[index];
      if (session.newName.trim()) {
        await api.post("chat_sys/update_session", {
          session_id: session.id,
          session_name: session.newName
        })
        session.editing = false;
        session.newName = "";
        console.log(`Session name updated: ${session.sessionName}`);
        await this.loadHistory()
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
