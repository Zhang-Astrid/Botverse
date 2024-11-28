<template>
  <div class="input-box">
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
  width: 80%;
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
</style>
