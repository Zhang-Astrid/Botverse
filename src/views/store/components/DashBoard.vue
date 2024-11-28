<template>
  <div class="dashboard">
    <div class="content">
      <GPTCard v-for="n in 1" :key="n" />
    </div>
  </div>
</template>

<script>
import GPTCard from "@/views/store/components/GPTCard.vue";

export default {
  name: "DashBoard",
  components: {
    GPTCard,
  },
};
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  padding: 20px;
  background-color: #1f2937;
  height: 100vh;
}

.content {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
}
</style>
