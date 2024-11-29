<template>
  <div class="sidebar">
    <div class="icon-list">
      <div v-for="icon in icons" :key="icon.id" class="icon-item">
        <img :src="icon.src" :alt="icon.alt" />
        <span class="icon-text">{{ icon.text }}</span> <!-- 添加文字 -->
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['getSharedData']),
    ...mapGetters(['getShared']),
  },
  created(){
    this.icons.push({ id: 1, src: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0fMCJkx2CKWiXE_fe36sVjv8M0cWZUk4Twg&s', alt: 'Icon 1', text: this.getShared.model_type } )// 添加文字字段
  },
  watch: {
    // 监听 getShared.model_type 的变化
    'getShared.model_type': function(newValue) {
      // 更新 icons 中的 text
      this.icons[0].text = newValue;
    }
  },
  data() {
    return {
      icons: [
        
      ]
    };
  }
};
</script>

<style>
.sidebar {
  width: 100px;
  background-color: #1e1e2f;
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
  align-items: center; /* 图标和文字居中 */
}

.icon-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center; /* 使文字和图标都居中 */
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

.icon-text {
  margin-top: 10px; /* 调整文字与图标的距离 */
  font-size: 12px;
  color: #ffffff; /* 文字颜色 */
}
</style>
