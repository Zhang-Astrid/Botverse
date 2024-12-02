<template>
  <div class="chat-box">
    <div v-for="(message, index) in messages" :key="index" class="message">
      <strong>{{ message.role === "user" ? this.getShared.username : this.getShared.model_name }}:</strong>
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
import axios from "axios";
import { mapActions, mapGetters } from 'vuex';
import katex from 'katex';  // 导入KaTeX

export default {
  computed: {
    ...mapGetters(['getSharedData']),
    ...mapGetters(['getShared']),
  },
  data() {
    return {
      username: "你",  // 用户名
      modelname: "机器人"  // 机器人名称
    }
  },
  props: {
    messages: {
      type: Array,
      required: true,
    },
  },
  methods: {
    // 渲染 Markdown 格式的文本，并处理数学公式
    renderMarkdown(text) {
      try {
        // 首先渲染常规的Markdown文本
        let html = marked(text || "");

        // 然后处理数学公式，使用KaTeX渲染公式
        html = this.renderMath(html);

        return html;
      } catch (err) {
        console.error("Markdown 渲染错误:", err);
        return text;
      }
    },

    // 渲染数学公式
    renderMath(html) {
      // 检测是否有公式需要包裹在 $ 符号里
      html = html.replace(/\\\((.*?)\\\)/g, (match, content) => {
        // 如果是 LaTeX 内联公式，包裹成 $...$
        return `\$${content}\$`;
      });

      html = html.replace(/\\\[(.*?)\\\]/gs, (match, content) => {
        // 如果是 LaTeX 块级公式，包裹成 $$...$$
        return `\$\$${content}\$\$`;
      });

      // 渲染内联数学公式：$ ... $
      html = html.replace(/\$(.*?)\$/g, (match, content) => {
        try {
          return katex.renderToString(content, { throwOnError: false });
        } catch (error) {
          console.error("KaTeX 渲染错误:", error);
          return match;
        }
      });

      // 渲染块级数学公式：$$ ... $$
      html = html.replace(/\$\$(.*?)\$\$/gs, (match, content) => {
        try {
          return `<div class="math-block">${katex.renderToString(content, { displayMode: true, throwOnError: false })}</div>`;
        } catch (error) {
          console.error("KaTeX 渲染错误:", error);
          return match;
        }
      });

      return html;
    },

    // 支持按钮的点击事件
    handleSupport(index) {
      console.log("支持消息:", this.messages[index]);
    },

    // 反对按钮的点击事件
    handleOppose(index) {
      console.log("反对消息:", this.messages[index]);
    },

    // 添加新的消息到消息列表
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
  background: #f7f9fc; /* 淡蓝色背景 */
  color: #333; /* 字体颜色 */
  border-radius: 8px; /* 圆角 */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* 阴影效果 */
  height: 100%;
}

.message {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #ffffff; /* 消息背景色为白色 */
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 消息框的阴影效果 */
}

.message-content {
  margin-left: 10px;
  word-wrap: break-word;
  font-size: 1rem;
}

.message-buttons {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}

.message-buttons button {
  padding: 8px 12px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s, transform 0.2s;
}

.message-buttons button:hover {
  background-color: #0056b3;
  transform: scale(1.1); /* 按钮悬浮时放大 */
}

.message-buttons button:active {
  background-color: #004085;
  transform: scale(0.95); /* 按钮按下时缩小 */
}

.message strong {
  font-weight: bold;
  color: #007bff; /* 发送者名称使用蓝色 */
}

.message-content p {
  margin: 5px 0;
  line-height: 1.6;
}

.math-block {
  margin: 20px 0;
  text-align: center;
  font-size: 1.2rem;
}
</style>
