<template>
  <div class="input-box">
    <!-- Forget Button -->
    <button @click="handleForget">Forget</button>
    <!-- Monocycle Button -->
    <button @click="togMonocycle">Monocycle</button>
    <!-- Message Input Box -->
    <input v-model="message" @keydown.enter="sendMessage" placeholder="Type your message..." />
    <button @click="sendMessage">Send</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: "", // 用户输入的消息
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
      // Forget按钮的功能暂时保留
      this.$emit("forget-message");
      console.log("Forget button clicked");
    },
    togMonocycle() {
      // 切换session_limit的值
      this.$emit("toggleMonocycle");
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
