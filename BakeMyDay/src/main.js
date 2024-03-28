import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import AOS from "aos";
import "aos/dist/aos.css";


const app = createApp(App)

app.use(router)

app.mount('#app')


// init AOS animation
AOS.init({
    duration: 1500,
    offset: 100,
});