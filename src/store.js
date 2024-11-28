import { createStore } from 'vuex';

export default createStore({
  state: {
    sharedData: 1
  },
  mutations: {
    updateSharedData(state, newData) {
      state.sharedData = newData;
    }
  },
  getters: {
    getSharedData: state => state.sharedData
  }
});