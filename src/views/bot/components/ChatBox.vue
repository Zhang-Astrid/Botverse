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
import {mapGetters} from 'vuex';
import {marked} from "marked";
import katex from "katex";
import api from "@/api/api.js";

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

    replaceLatexSymbols(text) {
  // 将 \[ 和 \] 替换为 $$，将 \( 和 \) 替换为 $
    // 替换 \) 为 $
      return text
      .replace(/\\\[/g, '$$')  // 替换 \[ 为 $$
      .replace(/\\\]/g, '$$')  // 替换 \] 为 $$
      .replace(/\\\(/g, '$')   // 替换 \( 为 $
      .replace(/\\\)/g, '$');
},
    // 渲染 Markdown 格式的文本，并处理数学公式
    renderMarkdown(text) {
  console.log("Before", text);
  try {
    // 首先替换文本中的图片链接
    text = this.renderImageUrls(text);

    // 替换 LaTeX 符号
    text = this.replaceLatexSymbols(text);

    // 渲染 KaTeX 数学公式
    text = this.renderKaTeX(text);
    console.log(text);

    // 先渲染常规的 Markdown 文本
    let html = marked(text || "");
    console.log("After Markdown render ", html);

    // 渲染 KaTeX 数学公式
    return html;
  } catch (err) {
    console.error("Markdown 渲染错误:", err);
    return text;
  }
},

// 渲染图片 URL 为 <img> 标签
renderImageUrls(text) {
  return text.replace(/(https?:\/\/[^\s]+(\.(jpg|jpeg|png|gif|bmp|svg|webp))(\?[^\s]*)?(\#[^\s]*)?)/g, (match, url) => {
    return `<img src="${url}" alt="image" class="message-image"/>`;
  });
}
,


// 处理 KaTeX 渲染的函数
renderKaTeX(html) {
  // 渲染块级公式
  html = html.replace(/\$\$([\s\S]+?)\$\$/g, (match, formula) => {
    try {
      return katex.renderToString(formula, { displayMode: true });
    } catch (e) {
      console.error("KaTeX 渲染错误:", e);
      return match; // 如果渲染失败，返回原始公式
    }
  });

  // 渲染行内公式
  html = html.replace(/\$([^\$]+?)\$/g, (match, formula) => {
    try {
      return katex.renderToString(formula, { displayMode: false });
    } catch (e) {
      console.error("KaTeX 渲染错误:", e);
      return match; // 如果渲染失败，返回原始公式
    }
  });

  return html;
}
,


    // 支持按钮的点击事件
    async handleSupport(index) {
      this.$message("已支持！")
      await api.post("/admin_sys/eval_and_click",{
        model_id: this.getShared.model_id,
        add_good_eval: 1
      })
      console.log("支持消息:", this.messages[index]);
    },

    // 反对按钮的点击事件
    async handleOppose(index) {
      this.$message("已反对！")
      console.log(this.getShared.model_id)
      await api.post("/admin_sys/eval_and_click",{
        model_id: this.getShared.model_id,
        add_bad_eval: 1
      })
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
