<template>
  <div class="input-box">
    <!-- Forget Button -->
    <button @click="handleForget" class="forget-btn">清除历史信息</button>
    <!-- Monocycle/Multicycle Button -->
    <button @click="togMonocycle" class="toggle-btn">{{ isMonocycle ? "切换到单轮模式" : "切换到记忆模式" }}</button>
    <!-- Message Input Box -->
    <input v-model="message" @keydown.enter="sendMessage" placeholder="输入消息..." class="message-input" />
    <button @click="sendMessage" class="send-btn">发送</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: "", // 用户输入的消息
      isMonocycle: true, // 初始状态为 Monocycle
    };
  },
  methods: {
    sendMessage() {
      if (this.message.trim()) {
        this.$emit("send-message", this.message);
        this.message = ""; // 清空输入框
      }
    },
    handleForget() {
      this.$emit("forget-message");
      console.log("Forget button clicked");
    },
    togMonocycle() {
      // 切换 isMonocycle 的值
      this.isMonocycle = !this.isMonocycle;
      this.$emit("toggleMonocycle", this.isMonocycle); // 传递当前状态
    },
  },
};
</script>

<style scoped>
.input-box {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background-color: #f7f9fc; /* 背景色为浅蓝 */
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  align-items: center;
}

.input-box button {
  padding: 10px 15px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
  font-size: 1rem;
}

.input-box .forget-btn {
  background-color: #ff6347; /* 清除按钮的颜色为番茄红 */
}

.input-box .forget-btn:hover {
  background-color: #e53e3e;
  transform: scale(1.05);
}

.input-box .toggle-btn {
  background-color: #007bff; /* 切换模式按钮的颜色 */
}

.input-box .toggle-btn:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}

.input-box .send-btn {
  background-color: #32cd32; /* 发送按钮的颜色为绿色 */
}

.input-box .send-btn:hover {
  background-color: #28a745;
  transform: scale(1.05);
}

.input-box .message-input {
  width: 50%;
  padding: 10px;
  background-color: #e1e8f0; /* 输入框背景色为淡蓝色 */
  color: #333;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
  margin-right: 10px;
}

.input-box .message-input:focus {
  outline: none;
  border-color: #007bff; /* 输入框获得焦点时的蓝色边框 */
}
</style>
