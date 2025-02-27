import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/HomePage.vue';
import Dashboard from '../components/DashboardPage.vue';  // 导入 Dashboard 组件

const routes = [
    {
        path: '/home',
        name: 'Home',
        component: Home
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { requiresAuth: true }  // 需要认证
    },
    {
        path: '/',
        redirect: '/login'
    }
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
});

// 路由守卫：检查用户是否已登录
router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth && !localStorage.getItem('token')) {
        next('/login');  // 如果没有登录，跳转到登录页面
    } else {
        next();
    }
});

export default router;
