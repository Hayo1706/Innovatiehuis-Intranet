import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'

import "./main.css"
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import ProjectsPage from './pages/manage/projects/ProjectsPage.vue';
import UsersPage from './pages/manage/users/UsersPage.vue';
import ProjectPage from './pages/project/ProjectPage.vue';
import ProjectSettingsPage from './pages/project/settings/ProjectSettingsPage.vue';
import UserPage from './pages/user/UserPage.vue';
import HomePage from './pages/home/HomePage.vue';
import LoginPage from './pages/login/LoginPage.vue';
import NotFoundPage from './pages/notfound/NotFoundPage.vue';
import ResetPasswordPage from './pages/manage/reset_password/ResetPasswordPage.vue';
import AccessControlView from "@/pages/manage/roles/AccessControlView";
import NoAccessPage from '@/pages/no_access/NoAccessPage.vue';
const routes = [
  { path: '', redirect: '/login' },
  { path: '/manage/projects', component: ProjectsPage },
  { path: '/manage/users', component: UsersPage },
  { path: '/manage/resetpassword', component: ResetPasswordPage },
  { path: '/manage/roles', component: AccessControlView },
  { path: '/project/:id', component: ProjectPage },
  { path: '/project/:id/:catchAll(.*)', component: ProjectPage },
  { path: '/project/:id/projectsettings', component: ProjectSettingsPage },
  { path: '/user/:id', component: UserPage },
  { path: '/home', component: HomePage },
  { path: '/login', component: LoginPage },
  { path: '/no_access', component: NoAccessPage },
  { path: '/:catchAll(.*)', component: NotFoundPage }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (!to.fullPath.includes('/login')) {
    localStorage.setItem("previousRoute", to.fullPath);
  }
  if (!localStorage.getItem("loggedIn") && !to.fullPath.includes('/login') && to.path !== "/manage/resetpassword") {
    localStorage.setItem("userWasRedirected", true);
    next({ path: '/login' });
  }
  next();
})
console.log(
  "%cBackground image",
  "display: inline-block ; background-image: url( https://bennadel.github.io/JavaScript-Demos/demos/console-log-css/rock.png ) ; " +
  "background-size: cover ; padding: 10px 175px 158px 10px ; " +
  "border: 2px solid black ; font-size: 11px ; line-height: 11px ; " +
  "font-family: monospace ;"
);
const app = createApp(App);
app.use(router);
app.mount('#app')
export default router;
