import {createApp} from 'vue';
import App from './App.vue';
import router from './router'; // 引入路由配置
import axios from 'axios';
//整体导入 ElementPlus 组件库
import ElementPlus from 'element-plus' //导入 ElementPlus 组件库的所有模块和功能
import 'element-plus/dist/index.css' //导入 ElementPlus 组件库所需的全局 CSS 样式
import store from './store.js';
const app = createApp(App);
app.use(store);
app.use(router);
app.use(ElementPlus);

//全局前置守卫
// router.beforeEach((to, from, next) => {
//     console.log("to:",to) //即将进入的路由的信息
//     console.log("from:",from) //当前即将离开的路由信息

//     next()

//     /*
//         if(to.name == "history"){
//             next(false) //拦截
//         }else{
//             next() //继续
//         }
//     */
// })


app.mount('#app')