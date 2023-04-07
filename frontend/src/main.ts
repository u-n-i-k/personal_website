import { createApp } from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

import App from './App.vue'
import i18n from "./i18n"
import router from './router'
import store from './store'

import './assets/main.css'

declare global {
  interface Window {
    grecaptcha: any;
  }
}

createApp(App).use(router).use(store).use(i18n).use(VueAxios, axios).mount('body');
