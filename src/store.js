import { createStore } from 'vuex';

export default createStore({
  state: {
    userid:10,
    username: 'n',
    gender: 'none',
    birthday: 'none',
    image: '',
    score:0,
  },
  mutations: {
    updateSharedData(state, newData) {
      state.userid = newData.user_id;
      state.username = newData.username;
      state.gender = newData.gender;
      state.birthday = newData.birthday;
      state.image = newData.image;
      state.score = newData.score;
    }
  },
  getters: {
    getSharedData: state => state.userid
  }
});