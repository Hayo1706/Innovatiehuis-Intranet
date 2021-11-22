import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'

import Allprojects from './adminpages/Allprojects.vue'
import Test from './Test.vue'


const routes = [
    { path: '/', component: Allprojects},
    { path: '/test', component: Test}
  ]
  const router = createRouter({
    history: createWebHistory(),
    routes
  })

const app  = createApp(App);
app.use(router);

app.mount('#app')
