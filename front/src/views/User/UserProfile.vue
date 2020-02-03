<template>
  <div>
    <v-list dark color="#110B22">
      <v-list-item>
        <v-avatar size="70">
          <img
            v-if="userInfo.picname!=='default'"
            :src="'../../assets/images/example/'+this.userInfo.picname"
          />

          <img v-else src="../../assets/images/profile_default.png" />
        </v-avatar>
        <v-spacer></v-spacer>
        <v-list-item-content>
          <h3>{{userInfo.likes}}</h3>
          <v-spacer></v-spacer>좋아요
        </v-list-item-content>

        <v-list-item-content @click="viewFollows()">
          <h3>{{userInfo.followings}}</h3>
          <v-spacer></v-spacer>팔로잉
        </v-list-item-content>
        <v-list-item-content @click="viewFollows()">
          <h3>{{userInfo.followers}}</h3>
          <v-spacer></v-spacer>팔로워
        </v-list-item-content>
      </v-list-item>
      <v-list-item>
        <v-list-item-content>
          <h2 class="white--text">
          {{userInfo.intro}}
          </h2>
       <h5 class="grey--text">
         {{userInfo.username}} 
         </h5>
        </v-list-item-content>
        <br />
        <br />
      </v-list-item>
      <!-- <v-list-item> -->
    </v-list>

    <v-tabs centered fixed dark background-color="transparent">
      <v-tabs-slider color="#71d087"></v-tabs-slider>

      <v-tab href="#tab-1">
        게시 피드
        <br />
        {{feed.post}}
      </v-tab>

      <v-tab href="#tab-2">
        좋아한 피드
        <br />
        {{feed.liked}}
      </v-tab>

      <v-tab href="#tab-3">
        관심사
        <br />
        {{feed.keywords}}
      </v-tab>

      <v-tab-item id="tab-1">
        <v-container>
          <Post :content="text" :isLiked="false" :isClipped="true" />
          <!-- <Post content="title2" image="cat1" :isLiked="true" :isClipped="false" /> -->
        </v-container>
      </v-tab-item>
      <v-tab-item id="tab-2">
        <v-container>
          <v-btn>click</v-btn>
        </v-container>
      </v-tab-item>
      <v-tab-item id="tab-3">
        <v-container>
          <v-btn>click 2</v-btn>
        </v-container>
      </v-tab-item>
    </v-tabs>

    <!-- </v-list-item> -->
    <!-- </v-list> -->
  </div>
</template>

<script>
import "../../assets/css/components.scss";
import "../../assets/css/common.scss";
import "../../assets/css/style.scss";
import "../../assets/css/user.scss";

import Post from "../../components/common/Post";
import UserApi from "../../apis/UserApi";

export default {
  name: "components",
  components: {
    Post
  },
  methods: {
    viewFollows() {
      console.log(this.userInfo.nickname);
      this.$router.push({ name: "팔로", params: this.nickname });
    }
  },
  created() {
    UserApi.requestUserProfile(this.$route.params.email, res => {
      //확인용 ..useless ...
      let sentData = JSON.stringify(res.data);
      console.log("프로필 정보 : "+JSON.stringify(res.data));
        this.userInfo.followers = parseInt(JSON.stringify(res.data.followers.length))+10;
        this.userInfo.followings = parseInt(JSON.stringify(res.data.followings.length))+563;

      this.userInfo.intro = res.data.intro;
      this.userInfo.nickname = res.data.nickname;
      this.userInfo.username = res.data.username;

    }),
      error => {
        this.$router.push({ path: "/404" });
      },
      // (this.userInfo.email = this.$route.params.email),
      (this.userInfo.likes = 1225),
      (this.feed.post = 3452),
      (this.feed.liked = 124),
      (this.feed.keywords = 45),
      (this.userInfo.picname = "default");

    //가라연합
    // (this.userInfo.followings = 875),
    // (this.userInfo.followers = 463),
    // (this.userInfo.intro = "홍주네 고양이를 보러오세용..!"),
    // this.userInfo.picname='moon_home.jpg'
    //   this.text='../../assets/images/'+this.userInfo.picname
  },

  data: () => {
    return {
      userInfo: {
        nickname: "",
        username: "",
        likes: "",
        followers: 0,
        followings: 0,
        picname: "",
        intro: ""
      },
      feed: {
        post: "",
        liked: "",
        keywords: ""
      },
      text:
        "이곳에 내용이 들어갑니다..... 내용상관없이 모든내용이 나올 예정스 라랄랄"
    };
  }
};
</script>

