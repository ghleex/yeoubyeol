<template>
  <div class="home" style="color: #EEEEEE; 
           text-align: center;">
    <!-- <img src="../assets/images/moon_home.jpg" alt /> -->
    <article>
      <div dark color="transparent" style="top: 60%; margin-top:70px">
        <h1>
          <br />달이 떴어요.
          <br />모두 나오세요.
          <br />
        </h1>
        <div v-if="!isOk">
          <v-btn text @click="tologin" class="white--text">로그인</v-btn>|
          <v-btn text @click="toConfirmEmail" class="white--text">회원가입</v-btn>
        </div>
        <div v-if="isOk">
          <v-btn text @click="goHome" class="white--text">홈으루</v-btn>|
          <v-btn text @click="logout" class="white--text">로그아웃</v-btn>
        </div>
      </div>
    </article>
    <!--  Video is muted & autoplays, placed after major DOM elements for performance & has an image fallback  -->
    <video autoplay loop id="video-background" muted plays-inline>
      <!-- <source :src="../assets/images/example/7.mp4" /> -->
      <source :src="homeVideo" />
    </video>
  </div>
</template>

<script>
import "../assets/css/home.scss";
import UserApi from "@/apis/UserApi";
import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();
export default {
  created() {
    this.setVideo();
    if (this.$cookies.isKey('refresh_cookie') && this.$cookies.isKey('auth_cookie') && this.$cookies.isKey('username')) {
      let refresh_token = this.$cookies.get('refresh_cookie')
      let auth_token = this.$cookies.get('auth_cookie')
      let username = this.$cookies.get('username')
      
      let userInfo = new FormData();
      userInfo.append('check', true)
      userInfo.append('username', username)
      userInfo.append('token_1', auth_token)
      userInfo.append('token_2', refresh_token)
      
      UserApi.requestLoginCheck(userInfo, response => {
        this.isOk = true
      }, error => {
        console.log('fxxk')
      })

    }
  },
  data: () => {
    return {
      isOk: false,
      homeVideo: ""
    };
  },

  methods: {
    setVideo() {
      let max = 6;
      let min = 1;
      let name = Math.floor(Math.random() * max) + min;
      this.homeVideo = require("@/assets/images/example/" + name + ".mp4");
    },
    logout() {
      let user = JSON.parse(sessionStorage.getItem("LoginUserInfo"))
      let userInfo = new FormData();
      userInfo.append('username', user.username)
      console.log(userInfo)
      axios.post(`http://${process.env.VUE_APP_IP}/accounts/logout/`, userInfo)
        .then(response => {
          console.log(response)
          sessionStorage.removeItem("AUTH_token");
          sessionStorage.removeItem("LoginUserInfo");
          this.$cookies.remove("auth_cookie");
          this.$cookies.remove("refresh_cookie");
          this.$cookies.remove("LoginUserInfo");
          this.$cookies.remove("username");
          alert("로그아웃되었습니다.");
          this.isOk = false;  
        })
    },
    tologin() {
      var router = this.$router;
      router.push({ name: "로그인" });
    },
    toConfirmEmail() {
      var router = this.$router;
      router.push({ name: "인증메일 발송" });
    },
    goHome() {
      var router = this.$router;
      router.push({ name: "메인피드" });
    }
  }
};
</script>
