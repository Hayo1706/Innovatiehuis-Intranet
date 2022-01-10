import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'

import "./main.css"
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import ProjectsPage from './pages/manage/projects/ProjectsPage.vue';
import UsersPage from './pages/manage/users/UsersPage.vue';
import ProjectPage from './pages/project/ProjectPage.vue';
import ProjectMembersPage from './pages/project/members/ProjectMembersPage.vue';
import ProjectSettingsPage from './pages/project/settings/ProjectSettingsPage.vue';
import UserPage from './pages/user/UserPage.vue';
import HomePage from './pages/home/HomePage.vue';
import LoginPage from './pages/login/LoginPage.vue';
import NotFoundPage from './pages/notfound/NotFoundPage.vue';
import ResetPasswordPage from './pages/manage/reset_password/ResetPasswordPage.vue';
const routes = [
  { path: '', redirect: '/login' },
  { path: '/manage/projects', component: ProjectsPage },
  { path: '/manage/users', component: UsersPage },
  { path: '/manage/resetpassword', component: ResetPasswordPage },
  { path: '/project/:id', component: ProjectPage },
  { path: '/project/:id/:catchAll(.*)', component: ProjectPage },
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

window.addEventListener('contextmenu', function (e) { 
  e.preventDefault(); 
}, false);

router.beforeEach((to, from, next) => {
  if (to.fullPath != "/login") {
    localStorage.setItem("previousRoute", to.fullPath);
  }
  if (!localStorage.getItem("loggedIn") && to.fullPath != "/login") {
    next({ path: '/login', params: { redirectMessage: "Uw sessie is verlopen, log opnieuw in." }});
  } else {
        //TODO 404 on acces with wrong role
        if (to.fullPath == "/manage/projects" && localStorage.getItem("may_read_any_project") != 1) {
          next({ path: '/404'});
          return;
        }
        if(to.fullPath == "/manage/users" && localStorage.getItem("may_read_any_user") != 1){
          next({ path: '/404'});
          return;
        }
    next();

  }
})
const app = createApp(App);
app.use(router);

app.mount('#app')
export default router;
