<template>
  <div class="home" style="color: #EEEEEE; 
           text-align: center;">
    <!-- <img src="../assets/images/moon_home.jpg" alt=""> -->
    <article>
      <h1>
        <br />달이 떴어요.
        <br />모두 나오세요.
        <br />
        <span v-if="!isOk">
          <a @click="tologin">로그인</a> |
          <a @click="toConfirmEmail">회원가입</a>
        </span>
        <span v-if="isOk">
          <a @click="goHome" id="goHome">홈으루</a> |
          <a @click="logout" id="logoutButton">로그아웃</a>
        </span>
      </h1>
    </article>
    <!--  Video is muted & autoplays, placed after major DOM elements for performance & has an image fallback  -->
    <video autoplay loop id="video-background" muted plays-inline>
      <source src="../assets/images/example/5r.mp4" />
    </video>
  </div>
</template>

<script>
import "../assets/css/home.scss";
export default {
  created() {
    if (sessionStorage.getItem("AUTH_token")) {
      this.isOk = true;
    }
  },
  data: () => {
    return {
      isOk: false
    };
  },

  methods: {
    logout() {
      sessionStorage.removeItem("AUTH_token");
      this.$cookies.remove("auth_cookie");
      alert("로그아웃되었습니다.");
      const logoutButton = document.getElementById("logoutButton");
      logoutButton.remove();
      this.isOk = true;
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
