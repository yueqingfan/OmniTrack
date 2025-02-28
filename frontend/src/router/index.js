import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/HomePage.vue';
import Dashboard from '../components/DashboardPage.vue';

const routes = [
    {
        path: '/home',
        name: 'Home',
        component: Home
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard
    },
    {
        path: '/',
        redirect: '/home' // 重定向到home页面
    }
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
});


export default router;