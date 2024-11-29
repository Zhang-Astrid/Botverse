<template>
  <div class="chat-box">
    <div v-for="(message, index) in messages" :key="index" class="message">
      <strong>{{ message.role === "user" ? "你" : "机器人" }}:</strong>
      <div v-html="renderMarkdown(message.text)" class="message-content"></div>

      <!-- 添加支持和反对按钮 -->
      <div v-if="message.role === 'bot' && message.text !== 'Ask me anything!'" class="message-buttons">
        <button @click="handleSupport(index)">👍</button>
        <button @click="handleOppose(index)">👎</button>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from "marked";

export default {
  props: {
    messages: {
      type: Array,
      required: true,
    },
  },
  methods: {
    // 渲染 Markdown 格式的文本
    renderMarkdown(text) {
      try {
        return marked(text || ""); // 渲染 Markdown 内容
      } catch (err) {
        console.error("Markdown 渲染错误:", err);
        return text;
      }
    },

    // 支持按钮的点击事件
    handleSupport(index) {
      console.log("支持消息:", this.messages[index]);
      // 暂时留空，待后续实现
    },

    // 反对按钮的点击事件
    handleOppose(index) {
      console.log("反对消息:", this.messages[index]);
      // 暂时留空，待后续实现
    },

    addMessage(newMessage) {
      this.messages.push(newMessage);
    },
  },
};
</script>

<style scoped>
.chat-box {
  padding: 20px;
  overflow-y: auto;
  background: #1e1e2f;
  color: white;
}

.message {
  margin-bottom: 10px;
}

.message-content {
  margin-left: 10px;
  word-wrap: break-word;
}

.message-buttons {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}

.message-buttons button {
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.message-buttons button:hover {
  background-color: #0056b3;
}
</style>
