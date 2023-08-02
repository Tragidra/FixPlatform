import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import * as VueRouter from 'vue-router'
import VueAxios from "vue-axios";
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import Calculate from "@/views/Calculate.vue";

const routes = [
    { path: '/', component: Calculate },
]
const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes,
})
const vuetify = createVuetify({
    components,
    directives,
})
const app = createApp(App)
app.use(router)
app.use(vuetify)
app.use(VueAxios, axios)
app.mount('#app')