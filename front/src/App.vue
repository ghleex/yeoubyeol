<template>
  <v-app style="background-color:#110b22;">
    <v-content v-if="isLogin">
      <hongjulab :username = usernickname />
    </v-content>

    <v-content v-if="!isLogin">
      <!-- Provides the application the proper gutter -->
  
      <router-view v-on:LoginUserData="LoginUserData"></router-view>
    </v-content>
  </v-app>
</template>

      
<script>
import hongjulab from "./components/hongjulab";
export default {
  name: "App",
  components: {
    hongjulab
  },
  data: () => ({
    isLogin: false,
    usernickname:'',
  }),
  updated() {
    // if (this.$cookies.isKey('auth_cookie')) {
    if (sessionStorage.getItem("AUTH_token")) {
      this.isLogin = true;
    } else {
      this.isLogin = false;
    } 
      // console.log('zz');
      this.usernickname = this.$store.state.nickname;
      // console.log(this.$store.state.nickname);
      // console.log(this.$store.getters.getnickname);
  },
  created() {
    this.$vuetify.theme.primary = "#ef51b5";
    // if (this.$cookies.isKey('auth_cookie')) {
    if (sessionStorage.getItem("AUTH_token")) {
      this.isLogin = true;
    }
    // this.$vuetify.theme.themes.dark.background="#4caf50"
  },
  methods:{
    LoginUserData:function(){
      alert('event')
    }

  }
};
</script>