<template>
  <v-app style="background-color:#110b22;">
    <v-content v-if="isLogin && userNickname">
      <hongjulab :pr_username="userNickname" />
       <router-view :key="$route.fullPath"></router-view>
      <v-dialog max-width="600px">
        <template v-slot:activator="{ on }">
          <v-btn fixed dark fab bottom right color="#71d087" v-on="on">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </template>

        <feedCreateUpdate />
      </v-dialog>
    </v-content>

    <v-content v-if="!isLogin">
      <!-- Provides the application the proper gutter -->
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

      
<script>
import hongjulab from "./components/hongjulab";
import feedCreateUpdate from "@/views/Feed/FeedCreateUpdate.vue";
export default {
  name: "App",
  components: {
    hongjulab,
    feedCreateUpdate
  },
  data: () => ({
    isLogin: false,
    userNickname: "",
    userId: ""
  }),
  updated() {
    if (sessionStorage.getItem("AUTH_token")) {
      this.isLogin = true;
    } else {
      this.isLogin = false;
    }

    if (sessionStorage.getItem("LoginUserInfo")) {
      console.log("session test -> ", sessionStorage.getItem("LoginUserInfo"));
      const parsedLoginUserInfo = JSON.parse(
        sessionStorage.getItem("LoginUserInfo")
      );
      this.userNickname = parsedLoginUserInfo.nickname;
      this.userId = parsedLoginUserInfo.id;
    } else {
      this.userNickname = "";
      this.userId = "";
    }
  },
  created() {
    this.$vuetify.theme.primary = "#ef51b5";
    if (sessionStorage.getItem("AUTH_token")) {
      this.isLogin = true;
    } else {
      this.isLogin = false;
    }
    if (sessionStorage.getItem("LoginUserInfo")) {
      const parsedLoginUserInfo = JSON.parse(
        sessionStorage.getItem("LoginUserInfo")
      );
      this.userNickname = parsedLoginUserInfo.nickname;
      this.userId = parsedLoginUserInfo.id;
    } else {
      this.userNickname = "";
      this.userId = "";
    }
    // this.$vuetify.theme.themes.dark.background="#4caf50"
  }
};
</script>