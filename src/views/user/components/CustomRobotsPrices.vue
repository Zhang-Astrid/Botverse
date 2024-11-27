<template>
  <div>
    <el-form ref="priceForm" :model="priceForm" label-width="120px">
      <el-form-item label="机器人名称">
        <el-input v-model="priceForm.robotName" placeholder="机器人名称"></el-input>
      </el-form-item>
      <el-form-item label="价格">
        <el-input type="number" v-model="priceForm.price" placeholder="价格"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="setPrice">设置价格</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'CustomRobotsPrices',
  data() {
    return {
      priceForm: {
        robotName: '',
        price: null
      }
    };
  },
  methods: {
    setPrice() {
      // 实现设置价格的逻辑
      console.log('设置价格:', this.priceForm);
    }
  }
};
</script>

<style scoped>
/* 样式内容 */
</style>