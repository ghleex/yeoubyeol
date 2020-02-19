<template>
  <v-app style="background-color:#110b22;">
    <v-content v-if="isLogin && userNickname">
      <Navbar v-on:logoutEvent="logoutEvent" />
       <router-view :key="$route.fullPath"></router-view>
    </v-content>

    <v-content v-if="!isLogin">
      <!-- Provides the application the proper gutter -->
      <router-view :key="$route.fullPath"></router-view>
    </v-content>

  </v-app>
  
</template>

      
<script>
import Navbar from "./components/Navbar";
import feedCreateUpdate from "@/views/Feed/FeedCreateUpdate.vue";
import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();
export default {
  name: "App",
  components: {
    Navbar,
  },
  data: () => ({
    isLogin: false,
    userNickname: "",
    userId: ""
  }),
  methods: {
    logoutEvent() {
      this.isLogin = false;
    }
  },
  updated() {
    if (this.$cookies.isKey('username') && this.$cookies.isKey('auth_cookie')) {
      this.isLogin = true;
    } else {
      this.isLogin = false;
    }

    if (this.$cookies.isKey('LoginUserInfo')) {
      const parsedLoginUserInfo = this.$cookies.get('LoginUserInfo')
      this.userNickname = parsedLoginUserInfo.nickname;
      this.userId = parsedLoginUserInfo.id;
    } else {
      this.userNickname = "";
      this.userId = "";
    }
  },
  created() {
    this.$vuetify.theme.primary = "#ef51b5";
    if (this.$cookies.isKey('username') && this.$cookies.isKey('auth_cookie')) {
      this.isLogin = true;
    } else {
      this.isLogin = false;
    }
    if (this.$cookies.isKey('LoginUserInfo')) {
      const parsedLoginUserInfo = this.$cookies.get('LoginUserInfo')
      this.userNickname = parsedLoginUserInfo.nickname;
      this.userId = parsedLoginUserInfo.id;
    } else {
      this.userNickname = "";
      this.userId = "";
    }
    if (this.$cookies.isKey('LoginUserInfo') && !sessionStorage.getItem('refresh_token')) {
      let auth_token = this.$cookies.get('auth_cookie');
      let username = this.$cookies.get('username');

      let form = new FormData();
      form.append('username', username)
      form.append('token_1', auth_token)
      axios.post(`${process.env.VUE_APP_IP}/accounts/check/`, form)
        .then(response => {
          let refresh_token = response.data.token_2;
          sessionStorage.setItem('refresh_token', refresh_token)
        })
    }
    // this.$vuetify.theme.themes.dark.background="#4caf50"
  },
};
</script>
