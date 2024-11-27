<template>
  <div class="gpt-card">
    <div class="gpt-header">
      <img src="@/img/logo.png" alt="GPT logo" class="gpt-logo" />
      <h2>GPT-4.0</h2>
    </div>
    <p>
      OpenAI's most powerful model. Stronger than GPT-3.5 in quantitative
      questions (math and physics), creative writing, and many other
      challenging tasks. Powered by GPT-4o. Context window has been...
    </p>
  </div>
</template>

<script>
export default {
  name: "GPTCard",
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
