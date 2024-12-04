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
  background-color: rgb(255, 255, 255); /* 背景色为浅蓝 */
  border-radius: 0 0 10px 10px;
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
  background-color: #4c5caf; /* 清除按钮的颜色为番茄红 */
  color: white;
}

.input-box .forget-btn:hover {
  background-color: #eee8aa;
  transform: scale(1.05);
  color: #4c5caf;
}

.input-box .toggle-btn {
  background-color: #4c5caf; /* 切换模式按钮的颜色 */
  color: white;
}

.input-box .toggle-btn:hover {
  background-color: #eee8aa;
  transform: scale(1.05);
  color: #4c5caf;
}

.input-box .send-btn {
  background-color: #4c5caf; /* 发送按钮的颜色为绿色 */
  color: white;
}

.input-box .send-btn:hover {
  background-color: #eee8aa;
  transform: scale(1.05);
  color: #4c5caf;
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
  border-color: #4c5caf; /* 输入框获得焦点时的蓝色边框 */
}
</style>
