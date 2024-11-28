<template>
  <div class="chat-box">
    <!-- 动态渲染传入的 messages -->
    <div class="message" v-for="(msg, index) in messages" :key="index">
      <div
        class="message-content"
        :class="{'bot-message': msg.role === 'bot', 'user-message': msg.role === 'user'}"
      >
        {{ msg.text }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    messages: {
      type: Array,
      required: true, // 确保调用时传递了 messages
    },
  },
};
</script>


<style scoped>
.chat-box {
  background-color: #2c2c38;
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  overflow-y: auto;
  border-radius: 10px;
}

.message {
  display: flex;
  margin-bottom: 10px;
  transition: transform 0.2s;
}

.message:hover {
  transform: scale(1.02);
}

.message-content {
  background-color: #424242;
  color: #ffffff;
  padding: 10px 15px;
  border-radius: 20px;
  max-width: 80%;
}

.bot-message {
  background-color: #3a3a56;
  align-self: flex-start;
}

.user-message {
  background-color: #ffa500;
  align-self: flex-end;
}
</style>
