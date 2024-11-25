InputBox.vue<template>
  <div class="chat-box">
    <div class="message" v-for="(msg, index) in messages" :key="index">
      <div class="message-content">{{ msg.text }}</div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      messages: [{ text: 'Chat with me~' }]
    };
  }
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
</style>
