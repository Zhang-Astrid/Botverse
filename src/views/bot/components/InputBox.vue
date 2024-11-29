<template>
  <div class="input-box">
    <!-- Forget Button -->
    <button @click="handleForget">清除历史信息</button>
    <!-- Monocycle/Multicycle Button -->
    <button @click="togMonocycle">{{ isMonocycle ? "切换到单轮模式" : "切换到记忆模式" }}</button>
    <!-- Message Input Box -->
    <input v-model="message" @keydown.enter="sendMessage" placeholder="Type your message..." />
    <button @click="sendMessage">发送</button>
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
  background-color: #2f2f3e;
}

.input-box input {
  width: 60%;
  padding: 10px;
  background-color: #444;
  color: white;
  border: none;
  border-radius: 5px;
}

.input-box button {
  padding: 10px;
  background-color: #ffa500;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.input-box button:nth-child(1), .input-box button:nth-child(2) {
  background-color: #ffa500;
  margin-right: 10px;
}
</style>
