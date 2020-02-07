import Vue from 'vue'
import App from './App.vue'
import Router from 'vue-router'
import routes from './routes'
import store from './vuex/store'
import vuetify from './plugins/vuetify'
import theme from './theme'

import VueResource from 'vue-resource'
import VueAuthenticate from 'vue-authenticate'
import VueAxios from 'vue-axios'
import axios from 'axios';
import VueCookies from 'vue-cookies'

Vue.config.productionTip = false
Vue.prototype.$EventBus = new Vue();

Vue.use(VueCookies)
Vue.use(VueAxios, axios)
Vue.use(VueAuthenticate, {
  baseUrl: 'http://192.168.31.87:8000',

  providers: {
    google: {
      clientId: '816014797066-epr1ld8dep07dat6na0mmcksdo6fv3s4.apps.googleusercontent.com',
      redirectUri: 'http://192.168.31.87:8000/',
      url: 'http://192.168.31.87:8000/api/login/social/token_user/google/',
      provider: 'google-oauth2'
    }
  }
});

Vue.use(Router)
Vue.use(vuetify,{theme})
const router = new Router({
    mode: 'history',
    routes,
});

new Vue({
    router,
    store,
    vuetify,
    render: h => h(App)
}).$mount('#app');


