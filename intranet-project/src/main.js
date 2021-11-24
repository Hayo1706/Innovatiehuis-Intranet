import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'

import "./main.css"
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import ProjectsPage from './pages/manage/projects/Main.vue';
import ProjectsCreatePage from './pages/manage/projects/create/Main.vue';
import UsersCreatePage from './pages/manage/users/create/Main.vue';
import UsersPage from './pages/manage/users/Main.vue';
import ProjectPage from './pages/project/Main.vue';
import ProjectMembersPage from './pages/project/members/Main.vue';
import ProjectSettingsPage from './pages/project/settings/Main.vue';
import UserPage from './pages/user/Main.vue';
import HomePage from './pages/home/Main.vue';
import NotFoundPage from './pages/notfound/Main.vue'

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
  { path: '/:catchAll(.*)', component: NotFoundPage }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App);
app.use(router);

app.mount('#app')
