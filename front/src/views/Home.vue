<template>
  <div class="home" style="color: #EEEEEE; 
           text-align: center;">
    <!-- <img src="../assets/images/moon_home.jpg" alt /> -->
    <article>
      <div dark color="transparent" style="top: 60%; margin-top:70px">
        <h1>
          <br>궂은 날에 잠깐
          <br>나왔다가 숨는 별.
        </h1>
   
        <div v-if="!isLogin">
          <v-btn text @click="tologin" class="white--text">로그인</v-btn>|
          <v-btn text @click="toConfirmEmail" class="white--text">회원가입</v-btn>
        </div>
        <div v-if="isLogin">
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
    if (this.$cookies.isKey('auth_cookie') && this.$cookies.isKey('username')) {
      this.isLogin = true
      // let refresh_token = this.$cookies.get('refresh_cookie')
      let auth_token = this.$cookies.get('auth_cookie')
      let username = this.$cookies.get('username')
      
      let userInfo = new FormData();
      // userInfo.append('check', true)
      userInfo.append('username', username)
      userInfo.append('token_1', auth_token)
      if (sessionStorage.getItem('refresh_token')) {
        let refresh_token = sessionStorage.getItem('refresh_token')
        userInfo.append('token_2', refresh_token)
      }
      // userInfo.append('token_2', null)
      
      UserApi.requestLoginCheck(userInfo, response => {
        this.isLogin = true
      }, error => {
      })

    }
  },
  data: () => {
    return {
      isLogin: false,
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
      let user = this.$cookies.get('username')
      let userInfo = new FormData();
      userInfo.append('username', user)
      axios.post(`${process.env.VUE_APP_IP}/accounts/logout/`, userInfo)
        .then(response => {
          sessionStorage.removeItem("refresh_token");
          this.$cookies.remove("auth_cookie");
          this.$cookies.remove("LoginUserInfo");
          this.$cookies.remove("username");
          this.$emit('logoutEvent')
          alert("로그아웃되었습니다.");
          this.isLogin = false;
        })
    },
    tologin() {
      let router = this.$router;
      router.push({ name: "로그인" });
    },
    toConfirmEmail() {
      let router = this.$router;
      router.push({ name: "인증메일 발송" });
    },
    goHome() {
      let router = this.$router;
      router.push({ name: "메인피드" });
    }
  }
};
</script>
