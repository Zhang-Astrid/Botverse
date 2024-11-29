import { createStore } from 'vuex';

export default createStore({
  state: {
    userid:10,
    username: 'n',
    gender: 'none',
    birthday: 'none',
    image: '',
    score:0,

    model_id: 0,
    model_name: 'nonw',
    model_type:"none",
    session_id: 0,
    session_name: 'nonw',
  },
  mutations: {
    updateSharedData(state, newData) {
      // 遍历state中的字段，并检查newData中是否存在
      for (const key in state) {
        if (newData.hasOwnProperty(key)) {
          // 如果newData中有对应的字段，则更新state中的值
          state[key] = newData[key];
        }
      }
    },
  },
  getters: {
    getSharedData: state => state.userid,
    getShared: state => state,
  }
});