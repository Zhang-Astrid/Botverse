import {createRouter, createWebHistory} from 'vue-router';


// 路由配置
const routes = [
    {
        path: "/",
        alias: ["/login", "/index"],
        // name: "Login",
        component: () => import("@/views/login/index.vue"),
    },
    {
        path: "/register",
        // name: "Register",
        component: () => import( "@/views/login/register.vue"),
        // meta: {title: 'Register - My App'},
    },
    {
        path: "/resetPswd",
        // name: "resetPswd",
        component: () => import( "@/views/login/resetPswd.vue"),
        // meta: {title: 'resetPassword - My App'},
    },
    {
        path: "/user",
        component: () => import ("@/views/user/user.vue")
    },
    {
        path: "/adminUser",
        component: () => import ("@/views/user/components/AdminPanel.vue")
    },
    {
        path: "/chatbot/session/:sessionId",
        component: () => import('@/views/bot/bot.vue')
    }
    ,
    {
        path: "/modelview",
        component: () => import('@/views/model/model.vue')
    },
    {
        path: "/choosebot",
        component: () => import('@/views/store/store.vue')
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


// import {createRouter, createWebHistory} from 'vue-router';
//
//
// const routes = [
//     {
//         path: '/',
//         alias:["/index","/login"],
//         component: () => import("../views/login/index.vue"),
//         name: "Login",
//     },
//     {
//         path: '/register',
//         component: () => import( '../views/login/userRegister.vue'),
//         name: 'Register',
//     },
//     {
//         path: '/resetPWD',
//         component: () => import( '../views/login/resetPassword.vue'),
//         name: 'ResetPWD',
//     }
// ]
//
// const router = createRouter({
//     history: createWebHistory(), // 使用 HTML5 History 模式
//     routes: routes
// });
//
// router.beforeEach(async (to, from, next) => {
//     NProgress.start();
//     // document.title = to.meta.title ? `${to.meta.title} - ${config.APP_NAME}` : `${config.APP_NAME}`;
//
//     // let token = tool.cookie.get("TOKEN");
//
//     if (to.path === "/login") {
//         router.addRoute(routes[0]);
//         routes_404_r();
//         isGetRouter = false;
//         next();
//         return false;
//     }
//
//     if (!token) {
//         next({ path: '/login' });
//         return false;
//     }
//
//     if (!isGetRouter) {
//         let apiMenu = tool.data.get("MENU") || [];
//         let userInfo = tool.data.get("USER_INFO");
//         let userMenu = treeFilter(userRoutes, node => {
//             return node.meta.role ? node.meta.role.filter(item => userInfo.role.indexOf(item) > -1).length > 0 : true;
//         });
//         let menuRouter = filterAsyncRouter([...userMenu, ...apiMenu]);
//         menuRouter.forEach(item => {
//             router.addRoute("layout", item);
//         });
//         routes_404_r = router.addRoute(routes_404);
//         isGetRouter = true;
//     }
//     beforeEach(to, from);
//     next();
// });
//
//
//
// export default router;
