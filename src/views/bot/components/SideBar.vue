<template>
  <div class="sidebar">
    <div class="icon-list">
      <div v-for="icon in icons" :key="icon.id" class="icon-item">
        <img :src="icon.src" :alt="icon.alt" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      icons: [
        { id: 1, src: 'path_to_icon1', alt: 'Icon 1' },
        { id: 2, src: 'path_to_icon2', alt: 'Icon 2' },
        { id: 3, src: 'path_to_icon3', alt: 'Icon 3' },
      ]
    };
  }
};
</script>

<style>
.sidebar {
  width: 100px;
  background-color: #24242e;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
  border: 0;
  margin: 0;
}

.icon-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.icon-item img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  transition: transform 0.2s;
}

.icon-item img:hover {
  transform: scale(1.1);
}
</style>
