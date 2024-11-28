<template>
  <button class="gpt-card" @click="navigateToChatbot">
    <div class="gpt-header">
      <img src="@/img/logo.png" alt="GPT logo" class="gpt-logo" />
      <h2>GPT-4o</h2>
    </div>
    <p>
      OpenAI的最强大模型，比GPT-3.5在定量问题（数学和物理）、创意写作等许多挑战性任务上更强大。由GPT-4o驱动，具有强大的上下文窗口...
    </p>
  </button>
</template>

<script>
export default {
  name: "GPTCard",
  methods: {
    navigateToChatbot() {
      // 使用 Vue Router 跳转到 /chatbot 页面，并刷新页面
      this.$router.push('/chatbot').then(() => {
        window.location.reload(); // 刷新页面
      });
    },
  },
};
</script>

<style scoped>
.gpt-card {
  background-color: #2e3b54;
  color: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 200px;
  margin: 10px;
  text-align: center;
  border: none;
  cursor: pointer;
}

.gpt-card:focus {
  outline: none;
}

.gpt-header {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
}

.gpt-logo {
  width: 40px;
  margin-right: 10px;
}

h2 {
  font-size: 1.2rem;
  margin: 0;
}
</style>
