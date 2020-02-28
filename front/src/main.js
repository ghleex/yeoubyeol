import Vue from 'vue'
import App from './App.vue'
import Router from 'vue-router'
import routes from './routes'
import store from './vuex/store'
import vuetify from './plugins/vuetify'
import theme from './theme'

import VueAxios from 'vue-axios'
import axios from 'axios';
import VueCookies from 'vue-cookies'

Vue.config.productionTip = false
Vue.prototype.$EventBus = new Vue();

Vue.use(VueCookies)
Vue.use(VueAxios, axios)

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


