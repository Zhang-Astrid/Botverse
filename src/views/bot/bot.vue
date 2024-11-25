<template>
  <div id="app">
    <div class="main-container">
      <Sidebar />
      <div class="content">
        <nav class="navbar">
          <ul>
            <li>Main</li>
            <li>Chat</li>
            <li>Bots</li>
            <li>Community</li>
            <li>Search</li>
          </ul>
        </nav>
        <div class="chat-section">
          <ChatBox />
          <InputBox @send-message="handleSendMessage" />
        </div>
      </div>
      <div class="history">
        <h3>History</h3>
        <!-- History content here -->
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/views/bot/components/SideBar.vue';
import ChatBox from '@/views/bot/components/ChatBox.vue';
import InputBox from '@/views/bot/components/InputBox.vue';

export default {
  components: { Sidebar, ChatBox, InputBox },
  methods: {
    handleSendMessage(message) {
      console.log('Message sent:', message);
    }
  }
};
</script>

<style>

* {
  padding: 0;
  margin: 0;
  border: 0;
  box-sizing: border-box; /* 确保宽度和高度包括内边距和边框 */
}


html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  border: 0;
  overflow: hidden;
}

#app {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  margin-top: 0;
}

.main-container {
  display: flex;
  flex-grow: 1;
  height: 100vh;
  width: 100vw;
  background-color: #1e1e2f;
}

.content {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow-y: hidden;
}

.navbar {
  display: flex;
  justify-content: space-around;
  padding: 20px;
  background-color: #1e1e2f;
}

.navbar ul {
  display: flex;
  list-style: none;
  gap: 20px;
}

.navbar li {
  color: #ffffff;
  cursor: pointer;
  transition: color 0.2s;
}

.navbar li:hover {
  color: #ffa500; /* A highlight color */
}

.chat-section {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  justify-content: space-between;
  overflow: hidden;
}

.history {
  width: 300px;
  background-color: #1e1e2f;
  padding: 20px;
  color: white;
  overflow-y: auto;
}
</style>
