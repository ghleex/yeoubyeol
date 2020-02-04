<template>
  <v-app style="background-color:#110b22;">
    <v-content v-if="isLogin && usernickname">
      <hongjulab :username = usernickname />
    </v-content>

    <v-content v-if="!isLogin">
      <!-- Provides the application the proper gutter -->
  
      <router-view></router-view>
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
    if (sessionStorage.getItem("AUTH_token")) {
      this.isLogin = true;
    } else {
      this.isLogin = false;
    } 

    if (sessionStorage.getItem("LoginUserNickname")) {
      this.usernickname = sessionStorage.getItem("LoginUserNickname");
      // console.log("app vue -> "+this.usernickname);
    } else {
      this.usernickname = '';
    } 

  },
  created() {
    this.$vuetify.theme.primary = "#ef51b5";
    if (sessionStorage.getItem("AUTH_token")) {
      this.isLogin = true;
    }else{
      this.isLogin=false;
    }
    if (sessionStorage.getItem("LoginUserNickname")) {
      this.usernickname = sessionStorage.getItem("LoginUserNickname");
    }else{
      this.usernickname='';
    }
    // this.$vuetify.theme.themes.dark.background="#4caf50"
  },
};
</script>