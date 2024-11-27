<template>
  <div class="input-box">
    <input v-model="input" type="text" placeholder="Input something or ask me any questions~" />
    <button @click="sendMessage">
      <img src="../../../img/sendicon.png" alt="Send" />
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      input: ''
    };
  },
  methods: {
    sendMessage() {
      if (this.input) {
        this.$emit('send-message', this.input);
        this.input = '';
      }
    }
  }
};
</script>

<style>
.input-box {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #333;
  border-radius: 10px;
}

input {
  flex: 1;
  padding: 10px;
  background-color: #4a4a4a;
  border: none;
  color: white;
  border-radius: 20px;
  margin-right: 10px;
  transition: background-color 0.3s;
}

input:focus {
  background-color: #5a5a5a;
  outline: none;
}

button {
  background: none;
  border: none;
  cursor: pointer;
}

button img {
  width: 24px;
  height: 24px;
}
</style>
