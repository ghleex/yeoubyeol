<template>
  <v-card class="overflow-hidden">
    <v-app-bar
      absolute
      color="#110B22"
      dark
      elevate-on-scroll
      v-if="$route.path !== '/404' && $route.path !== '/error' && $route.path !== '/'"
    >
      <v-app-bar-nav-icon @click="drawer =!drawer"></v-app-bar-nav-icon>

      <v-toolbar-title>{{pageTitle}}</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn text icon>
        <v-icon @click="changeView('검색')" v-if="!isSearchPage">mdi-magnify</v-icon>
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app clipped color="#110B22" dark>
      <v-list>
        <v-list-item>
          <v-spacer></v-spacer>
          <v-btn text color="#71d087">통계</v-btn>
          <!-- <router-link to="/noti"> -->
          <v-btn text color="#71d087" @click="changeView('알림')">알림</v-btn>
          <!-- </!-->
        </v-list-item>

        <v-list-item>
          <v-list-item-avatar size="62"  color="grey darken-3">
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
        <v-list-item @click="changeViewProfile('팔로',currUserInfo.nickname)">
          <v-content class="left">{{currUserInfo.followers}} 팔로워</v-content>
          <v-spacer></v-spacer>
          <v-content>{{currUserInfo.followings}} 팔로잉</v-content>
        </v-list-item>

        <v-divider></v-divider>
        <v-list-item link>
          <v-list-item-content @click="changeView('메인피드')">메인피드</v-list-item-content>
        </v-list-item>
        <v-list-item link>
          <v-list-item-content>트렌드</v-list-item-content>
        </v-list-item>
        <v-list-item link>
          <v-list-item-content>큐레이션 피드</v-list-item-content>
        </v-list-item>
        <v-list-item link>
          <v-list-item-content>스크랩 된 피드</v-list-item-content>
        </v-list-item>
        <v-list-item link>
          <v-list-item-content>스킵 된 피드</v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>
        <v-list-item link>
          <v-list-item-content>설정</v-list-item-content>
        </v-list-item>
        <v-list-item link>
          <v-list-item-content @click="logout">로그아웃</v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-sheet>
      <v-container style="background-color:#110b22">
        <router-view></router-view>
      </v-container>
    </v-sheet>
  </v-card>
</template>

      
<script>
import UserApi from "../apis/UserApi";

export default {
  props: ["pr_username"],

  data: () => ({
    profileUsername: "",
    drawer: null,
    item: 0,
    pageTitle: "",

    isSearchPage: false,
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
    if (this.$route.name === "프로필") {
      this.pageTitle = this.$route.params.email;
    } else {
      this.pageTitle = this.$route.name;
    }
  },
  created() {
    //이거 선행님이 바꾼거 밑에 넣어야해
    if (this.$route.name === "검색") {
      this.isSearchPage = true;
    } else {
      this.isSearchPage = false;
    }

    //가라천국....heaven
    // this.$vuetify.theme.dark = true
    if (this.$route.name !== "프로필") {
      this.pageTitle = this.$route.name;
    } else {
      //프로필 화면인 경우에는 아이디를 상단에 노출시킴
      this.pageTitle = this.profileUsername;
    }

    //프로필 정보를 불러올거에여~~!
    UserApi.requestUserProfile(this.pr_username, res => {
      //확인용 ..useless ...
      let sentData = JSON.stringify(res.data);
      console.log("프로필 정보 : " + JSON.stringify(res.data));
      this.currUserInfo.followers = JSON.stringify(res.data.followers.length);
      this.currUserInfo.followings = JSON.stringify(res.data.followings.length);

      this.currUserInfo.intro = res.data.intro;
      this.currUserInfo.nickname = res.data.nickname;
      this.currUserInfo.username = res.data.username;
      // console.log('pic name is ',res.data.pic_name);
      this.currUserInfo.picname = require("@/assets/images/profile/" +
        res.data.pic_name +
        ".png");
    }),
      err => {
        this.$router.push({ path: "/404" });
      };
  },
  methods: {
    //path와 닉넴을받으면 프로필로 기기
    changeViewProfile(path, usersEmail) {
      this.pageTitle = usersEmail;
      this.$router.push({ name: path, params: { email: usersEmail } });
    },
    //그냥 이동일 경우
    changeView(path) {
      this.pageTitle = path;
      this.$router.push({ name: path });
    },
    logout() {
      sessionStorage.removeItem("AUTH_token");
      sessionStorage.removeItem("LoginUserInfo");
      this.$cookies.remove("auth_cookie");
      alert("로그아웃되었습니다.");
      this.$router.push({ name: "홈" });
    }
  }
};
</script>