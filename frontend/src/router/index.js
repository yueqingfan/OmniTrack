import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/HomePage.vue';
import Dashboard from '../components/DashboardPage.vue';
import AlarmRecords from "@/components/AlarmRecords.vue";
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
        path:'/alarmrecords',
        name:'AlarmRecords',
        component: AlarmRecords
    },
    {
        path: '/',
        redirect: '/home'
    }
];

const router = createRouter({
    history: createWebHistory(
        process.env.NODE_ENV === 'production' ? '/OmniTrack/' : process.env.BASE_URL
    ),
    routes
});

export default router;