import {createRouter, createWebHistory} from 'vue-router';


// 路由配置
const routes = [
    {
        path: "/",
        alias: ["/login", "/index"],
        // name: "Login",
        component: () => import("@/views/login/index.vue"),
    },
    // {
    //     path: "/register",
    //     // name: "Register",
    //     component: () => import( "@/views/login/register.vue"),
    //     // meta: {title: 'Register - My App'},
    // },
    // {
    //     path: "/resetPswd",
    //     // name: "resetPswd",
    //     component: () => import( "@/views/login/resetPswd.vue"),
    //     // meta: {title: 'resetPassword - My App'},
    // },
    {
        path: "/user",
        component: () => import ("@/views/user/user.vue")
    },
    {
        path: "/adminUser",
        component: () => import ("@/views/user/components/AdminPanel.vue")
    },
    {
        path: "/chatbot",
        component: () => import('@/views/bot/bot.vue')
    },
    {
        path: "/modelview",
        component: () => import('@/views/model/model.vue')
    },
    {
        path: "/choosebot",
        component: () => import('@/views/store/store.vue')
    },
    {
        path:"/forum",
        component:()=>import('@/views/forum/forum.vue')
    },
    {
        path:"/home",
        component:()=> import('@/views/Home.vue')
    }
    ]
// {
//     path: '/resetPSD',
//     name: 'resetPSD',
//     component: resetPSD,
//     meta: {title: 'Find Password - My App'},
// },
// {
//     path: '/main',
//     name: 'Main',
//     component: Main,
//     meta: { title: 'Main - My App' },
//     children: [
//         {
//             path: 'bot',
//             name: 'Bot',
//             component: Bot,
//             meta: { title: 'Bot - My App' },
//         },
//         {
//             path: 'store',
//             name: 'Store',
//             component: Store,
//             meta: { title: 'Store - My App' },
//         },
//         {
//             path: 'mypage',
//             name: 'MyPage',
//             component: MyPage,
//             meta: { title: 'My Page - My App' },
//         },
//     ],
// },


// 创建路由器实例
const router = createRouter({
    history: createWebHistory(),
    routes
})

// 路由守卫：动态设置页面标题
// router.beforeEach((to, from, next) => {
//     document.title = to.meta.title || 'My App';
//     next();
// });

export default router;
