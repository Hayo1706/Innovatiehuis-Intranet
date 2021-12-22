import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'

import "./main.css"
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import ProjectsPage from './pages/manage/projects/ProjectsPage.vue';
import ProjectsCreatePage from './pages/manage/projects/create/ProjectsCreatePage.vue';
import UsersCreatePage from './pages/manage/users/create/UsersCreatePage.vue';
import UsersPage from './pages/manage/users/UsersPage.vue';
import ProjectPage from './pages/project/ProjectPage.vue';
import ProjectMembersPage from './pages/project/members/ProjectMembersPage.vue';
import ProjectSettingsPage from './pages/project/settings/ProjectSettingsPage.vue';
import UserPage from './pages/user/UserPage.vue';
import HomePage from './pages/home/HomePage.vue';
import LoginPage from './pages/login/LoginPage.vue';
import NotFoundPage from './pages/notfound/NotFoundPage.vue';

const routes = [
  { path: '', redirect: '/home' },
  { path: '/manage/projects', component: ProjectsPage },
  { path: '/manage/projects/create', component: ProjectsCreatePage },
  { path: '/manage/users', component: UsersPage },
  { path: '/manage/users/create', component: UsersCreatePage },
  { path: '/project/:id', component: ProjectPage },
  { path: '/project/:id/settings', component: ProjectSettingsPage },
  { path: '/project/:id/members', component: ProjectMembersPage },
  { path: '/user/:id', component: UserPage },
  { path: '/home', component: HomePage },
  { path: '/login', component: LoginPage },
  { path: '/:catchAll(.*)', component: NotFoundPage }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {

  if (localStorage.getItem("token") == null && to.fullPath != "/login") {
    localStorage.setItem("previousRoute", to.fullPath);
    next({ path: '/login' });
  } else {
    next();
  }
})
const app = createApp(App);
app.use(router);

app.mount('#app')
