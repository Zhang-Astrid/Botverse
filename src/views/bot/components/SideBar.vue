<template>
  <div class="sidebar">
    <div class="icon-list">
      <div v-for="icon in icons" :key="icon.id" class="icon-item">
        <img :src="icon.src" :alt="icon.alt" />
      </div>
    </div>
    <button class="more-button" @click="navigateToChooseBot">More</button>
  </div>
</template>


<script>
export default {
  data() {
    return {
      icons: [
        { id: 1, src: 'src/img/ChatGPT_logo.svg.png', alt: 'Icon 1' }
      ]
    };
  },
  methods: {
    navigateToChooseBot() {
      // 方法一：直接跳转并刷新页面
      // window.location.href = '/choosebot';

      // 方法二：Vue Router 跳转并刷新
      this.$router.push('/choosebot').then(() => {
        window.location.reload();
      });
    }
  }
};
</script>

<style>
.more-button {
  margin-top: auto; /* 将按钮放在底部 */
  padding: 10px 20px;
  color: #ffffff;
  background-color: #3b3b4f;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.more-button:hover {
  background-color: #57576d;
}

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
