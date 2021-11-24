import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'

import "./main.css"
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import Allprojects from './pages/adminpages/projects/Allprojects.vue'
import Test from './pages/test/Test.vue'
import Project from './pages/test/Project.vue'



const routes = [
  { path: '/', component: Allprojects },
  { path: '/test', component: Test },
  { path: '/project', component: Project }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App);
app.use(router);

app.mount('#app')
