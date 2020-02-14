<template>
  <v-app style="background-color:#110b22;">
    <v-content v-if="isLogin && userNickname">
      <hongjulab/>
       <router-view :key="$route.fullPath"></router-view>
<!--       <v-dialog max-width="600px">
        <template v-slot:activator="{ on }">
          <v-btn fixed dark fab bottom right color="#71d087" v-on="on">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </template>

     
        <feedCreateUpdate />
      </v-dialog> -->
    </v-content>

    <v-content v-if="!isLogin">
      <!-- Provides the application the proper gutter -->
      <router-view :key="$route.fullPath"></router-view>
    </v-content>

  </v-app>
  
</template>

      
<script>
import hongjulab from "./components/hongjulab";
import feedCreateUpdate from "@/views/Feed/FeedCreateUpdate.vue";
import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();
export default {
  name: "App",
  components: {
    hongjulab,
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
      axios.post(`http://${process.env.VUE_APP_IP}/accounts/check/`, form)
        .then(response => {
          let refresh_token = response.data.token_2;
          sessionStorage.setItem('refresh_token', refresh_token)
          alert('세션에 저장했어용')
        })
    }
    // this.$vuetify.theme.themes.dark.background="#4caf50"
  },
};
</script>
