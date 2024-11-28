<template>
  <div class="chat-box">
    <div v-for="(message, index) in messages" :key="index" class="message">
      <strong>{{ message.role === "user" ? "你" : "机器人" }}:</strong>
      <div v-html="renderMarkdown(message.text)" class="message-content"></div>
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
    // 渲染 Markdown 格式的文本
renderMarkdown(text) {
  try {
    return marked(text || ""); // 渲染 Markdown 内容
  } catch (err) {
    console.error("Markdown 渲染错误:", err);
    return text;
  }
}
,
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
</style>
