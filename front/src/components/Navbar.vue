<template>
  <v-card class="overflow-hidden">
    <v-app-bar
      color="#110B22"
      dark
      elevate-on-scroll
      v-if="$route.path !== '/404' && $route.path !== '/error' && $route.path !== '/'"
    >
      <v-app-bar-nav-icon @click="drawer =!drawer"></v-app-bar-nav-icon>

      <v-toolbar-title>{{pageTitle}}</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn text icon v-if="!isPostPage && enableTime">
        <v-icon @click="changeViewPost('새 피드 작성')">mdi-pencil-plus-outline</v-icon>
      </v-btn>
      <v-btn text icon v-if="!isSearchPage">
        <v-icon @click="changeView('검색')">mdi-magnify</v-icon>
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app clipped color="#110B22" dark>
      <v-list>
        <v-list-item v-if="hasNewNoti">
          <v-spacer></v-spacer>
          <v-badge offset-x="13" offset-y="13" color="pink" dot>
            <v-btn text color="#71d087" @click="changeView('알림')">알림</v-btn>
          </v-badge>
        </v-list-item>
        <v-list-item v-else>
          <v-spacer></v-spacer>
          <v-btn text color="#71d087" @click="changeView('알림')">알림</v-btn>
        </v-list-item>

        <v-list-item>
          <v-list-item-avatar size="62" color="#110b22">
            <v-img :src="currUserInfo.picname"></v-img>
          </v-list-item-avatar>

          <v-list-item-content>
            <h1
              class="title"
              @click="changeViewProfile('프로필',currUserInfo.nickname)"
            >{{currUserInfo.nickname}}</h1>
            <v-list-item-subtitle>{{currUserInfo.username}}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item @click="changeViewProfile('팔로', currUserInfo.nickname)">
          <v-list-item-content class="left">{{currUserInfo.followers}} 팔로워</v-list-item-content>
          <v-spacer></v-spacer>
          <v-list-item-content>{{currUserInfo.followings}} 팔로잉</v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>
        <v-list-item link>
          <v-list-item-content @click="changeView('메인피드')">메인피드</v-list-item-content>
        </v-list-item>
        <v-list-item link>
          <v-list-item-content @click="changeView('트렌드')">트렌드</v-list-item-content>
        </v-list-item>
        <v-list-item link>
          <v-list-item-content @click="changeView('명예의 전당')">명예의 전당</v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>
        <v-list-item link>
          <v-list-item-content @click="changeViewProfileSetting('프로필 변경', currUserInfo.nickname)">설정</v-list-item-content>
        </v-list-item>
        <v-list-item link>
          <v-list-item-content @click="logout">로그아웃</v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- <v-sheet style="background-color:#110b22">
      <v-responsive style="background-color:#110b22">
       <router-view :key="$route.fullPath"></router-view>
      </v-responsive>
    </v-sheet>-->
  </v-card>
</template>

      
<script>
import UserApi from "../apis/UserApi";
import axios from "axios";
import dotenv from "dotenv";

dotenv.config();
export default {
  data: () => ({
    enableTime: true,

    profileUsername: "",
    drawer: null,
    item: 0,
    pageTitle: "",
    loginedNickname: "",
    isSearchPage: false,
    isPostPage: false,
    hasNewNoti: false,
    currUserInfo: {
      nickname: "로그인 에러",
      username: "잠시 후에 다시 시도해주세요",
      likes: "",
      followers: 0,
      followings: 0,
      picname: "",
      intro: ""
    }
  }),
  updated() {
    if (this.drawer) {
      this.getLoginUserProfile();
      this.getNotiUnread();
    }
    //time check
      const curr = new Date();
    if (curr.getHours() >= 11 && curr.getHours() < 17) {
      this.enableTime = true;
    } else {
      this.enableTime = false;
    }

    if (this.$route.name === "프로필") {
      this.pageTitle = this.$route.params.email;
    } else if (this.$route.name == "검색 결과") {
      this.pageTitle = "검색 결과 : " + this.$route.params.keyword;
    } else {
      this.pageTitle = this.$route.name;
    }
    // this.getLoginUserProfile();

    //이거 선행님이 바꾼거 밑에 넣어야해
    if (this.$route.name === "검색") {
      this.isSearchPage = true;
    } else {
      this.isSearchPage = false;
    }
    if (
      this.$route.name === "새 피드 작성" ||
      this.$route.name === "피드 수정"
    ) {
      this.isPostPage = true;
    } else {
      this.isPostPage = false;
    }
  },
  created() {
    //time check
    const curr = new Date();
    if (curr.getHours() >= 11 && curr.getHours() < 17) {
      this.enableTime = true;
    } else {
      this.enableTime = false;
    }
    //가라천국....heaven
    // this.$vuetify.theme.dark = true
    if (this.$route.name !== "프로필") {
      this.pageTitle = this.$route.name;
    } else if (this.$route.name == "검색 결과") {
      this.pageTitle = "검색 결과 : " + this.$route.params.keyword;
    } else {
      //프로필 화면인 경우에는 아이디를 상단에 노출시킴
      this.pageTitle = this.profileUsername;
    }
    this.getLoginUserProfile();
  },
  methods: {
    getNotiUnread() {
      if (this.$cookies.isKey("LoginUserInfo")) {
        let userInfo = this.$cookies.get("LoginUserInfo");
        let loginID = userInfo.id;
        UserApi.requestNonreadNotification(
          loginID,
          res => {
            if (res.data.not_read) {
              this.hasNewNoti = true;
            } else {
              this.hasNewNoti = false;
            }
          },
          error => {
            this.hasNewNoti = false;
          }
        );
      }
    },
    //path와 닉넴을받으면 프로필로 기기
    getLoginUserProfile() {
      //프로필 정보를 불러올거에여~~!
      if (this.$cookies.isKey("LoginUserInfo")) {
        let userInfo = this.$cookies.get("LoginUserInfo");
        this.loginedNickname = userInfo.nickname;
      }

      UserApi.requestUserProfile(
        this.loginedNickname,
        res => {
          //확인용 ..useless ...
          let sentData = JSON.stringify(res.data);
          this.currUserInfo.followers = JSON.stringify(
            res.data.followers.length
          );
          this.currUserInfo.followings = JSON.stringify(
            res.data.followings.length
          );
          this.currUserInfo.intro = res.data.intro;
          this.currUserInfo.nickname = res.data.nickname;
          this.currUserInfo.username = res.data.username;
          this.currUserInfo.picname = `${process.env.VUE_APP_IP}${res.data.pic_name}`;
        },
        err => {
          this.$router.push({ path: "/error" });
        }
      );
    },
    changeViewProfile(path, usersEmail) {
      this.drawer = !this.drawer;
      this.pageTitle = usersEmail;
      // this.$router.push({ name: path, params: { email: usersEmail } });
       this.$router.replace({
        name:path,
        params:{
          email:usersEmail
        }
      }).catch(err =>{
        this.drawer = false;
      })
    },
    changeViewProfileSetting(path, usersEmail) {
      if (this.pageTitle == "프로필 변경") {
        this.drawer = !this.drawer;
      } else {
        this.pageTitle = usersEmail;
        this.$router.push({ name: path, params: { email: usersEmail } });
      }
    },
    changeViewPost(path) {
      this.pageTitle = path;
      this.$router.push({ name: path, params: { postId: -1 } });
    },
    //그냥 이동일 경우
    changeView(path) {
      this.pageTitle = path;
      // this.$router.push({ name: path });
      this.$router.replace({
        name:path,
      }).catch(err =>{
        this.drawer = false;
      })
    },
    logout() {
      let user = this.$cookies.get("username");
      let userInfo = new FormData();
      userInfo.append("username", user);
      axios.post(`${process.env.VUE_APP_IP}/accounts/logout/`, userInfo)
        .then(response => {
          sessionStorage.removeItem("refresh_token");
          this.$cookies.remove("auth_cookie");
          this.$cookies.remove("LoginUserInfo");
          this.$cookies.remove("username");
          this.$emit("logoutEvent");
          this.isLogin = false;
        })
        .then(result => {
          alert("로그아웃되었습니다.");
          this.changeView("홈");
        });
    }
  }
};
</script>