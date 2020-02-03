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
      
      <v-btn text icon v-if="!profilePage.status">
        
        <v-icon @click="changeView('검색')"
        v-if="!isSearchPage"
        >mdi-magnify</v-icon>
      </v-btn>
      <v-btn text style="color:#71d087" v-else-if="profilePage.isMyprofile">설정</v-btn>
      <v-btn
        text
        style="color:#cc6666"
        v-else-if="!profilePage.isMyprofile && profilePage.isFollowed"
      >팔로우 끊기</v-btn>
      <v-btn
        text
        style="color:#71d087"
        v-else-if="!profilePage.isMyprofile && !profilePage.isFollowed"
      >팔로우</v-btn>
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
          <v-list-item-avatar size="62">
            <v-img src="../assets/images/example/cat1.jpg"></v-img>
          </v-list-item-avatar>

          <v-list-item-content>
            <h1 class="title" @click="changeViewProfile('프로필',userInfo.nickname)">{{userInfo.nickname}}</h1>
            <v-list-item-subtitle>{{userInfo.username}}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-content class="left">{{userInfo.followers}} 팔로워</v-content>
          <v-spacer></v-spacer>
          <v-content>{{userInfo.followings}} 팔로잉</v-content>
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
          <v-list-item-content>Language</v-list-item-content>
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
import UserApi from '../apis/UserApi'

export default {
  props:['username1'],

  data: () => ({
    drawer: null,
    item: 0,
    pageTitle: "",
    profilePage: {
      status: false,
      isMyProfile: "",
      isFollowed: ""
    },
    isSearchPage:false,
     userInfo: {
        nickname: "",
        username: "",
        likes: "",
        followers: 0,
        followings: 0,
        picname: "",
        intro: ""
      },
  }),
  updated() {
    this.pageTitle = this.$route.name
  },
  created() {
    //이거 선행님이 바꾼거 밑에 넣어야해 
    if(this.$route.name==='검색'){
      this.isSearchPage=true;
    }
    else{
      this.isSearchPage=false;
    }
    //가라천국....heaven
    // this.$vuetify.theme.dark = true
    if (this.$route.name !== "프로필") {
      this.pageTitle = this.$route.name;
      this.profilePage.status = false;
    } else {
      //프로필 화면인 경우에는 아이디를 상단에 노출시킴
      this.pageTitle = this.username;
      this.profilePage.status = true;
      if (this.username == this.userInfo.nickname) {
        //내 닉네임과 현재 조회 프로필닉네임가 같으면
        this.profilePage.isMyProfile = true;
      } else {
        this.profilePage.isMyProfile = false;
        //만약 내 친구야?
        this.profilePage.isFollowed = true;
      }
    }

  //프로필 정보를 불러올거에여~~!
    // UserApi.requestUserProfile(this.username, res => {
    //   //확인용 ..useless ...
    //   let sentData = JSON.stringify(res.data);
    //   console.log("프로필 정보 : "+JSON.stringify(res.data));
    //     this.userInfo.followers = parseInt(JSON.stringify(res.data.followers.length))+10;
    //     this.userInfo.followings = parseInt(JSON.stringify(res.data.followings.length))+563;

    //   this.userInfo.intro = res.data.intro;
    //   this.userInfo.nickname = res.data.nickname;
    //   this.userInfo.username = res.data.username;

    // }),
    //   error => {
    //     this.$router.push({ path: "/404" });
    //   }

  },
  methods:{
    //path와 이메일을받으면 프로필로 기기
    changeViewProfile(path,usersEmail){
      this.pageTitle=usersEmail;
    this.$router.push({ name: path, params: { email: usersEmail }})
    },
    //그냥 이동일 경우
    changeView(path){
      this.pageTitle=path;
this.$router.push({ name: path})
    }
  },
};
</script>