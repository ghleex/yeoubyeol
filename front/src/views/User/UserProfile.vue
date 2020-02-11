<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <v-col cols="12">
        <v-list dark color="#110B22">
          <v-list-item>
            <v-avatar size="70" color="grey darken-3">
              <v-img :src="userInfo.picname"></v-img>
            </v-avatar>
            <v-spacer></v-spacer>
            <v-list-item-content>
              <h3>{{userInfo.likes}}</h3>
              <v-spacer></v-spacer>좋아요
            </v-list-item-content>
            <v-list-item-content @click="viewFollows()">
              <h3>{{userInfo.followers}}</h3>
              <v-spacer></v-spacer>팔로워
            </v-list-item-content>

            <v-list-item-content @click="viewFollows()">
              <h3>{{userInfo.followings}}</h3>
              <v-spacer></v-spacer>팔로잉
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-spacer></v-spacer>
            <v-btn
              v-if="!isMyAccount"
              min-width="190"
              small
              color="#71d087"
              :style="setFollowBtn"
              @click="clickFollowBtn"
              :outlined="isFollow"
            >{{isFollow? "unFollow" : "Follow"}}</v-btn>
            <v-btn v-else min-width="190" small color="#71d087" outlined>setting profile</v-btn>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <h2 class="white--text">{{userInfo.intro}}</h2>
            </v-list-item-content>
            <br />
            <br />
          </v-list-item>
          <!-- <v-list-item> -->
        </v-list>

        <v-tabs centered fixed dark background-color="transparent">
          <v-tabs-slider color="#71d087"></v-tabs-slider>

          <v-tab href="#tab-1">
            게시한 피드
            <br />
            {{myArticles.length}}
          </v-tab>

          <v-tab href="#tab-2">
            좋아한 피드
            <br />
            {{myArticles.length}}
          </v-tab>

          <v-tab-item id="tab-1">
            <v-row class="pt-0" align="start" justify="center" style="background-color:#110b22">
              <v-col cols="12" v-for="article in myArticles" :key="article.id">
                <Post v-bind="article" />
              </v-col>
            </v-row>
          </v-tab-item>

          <v-tab-item id="tab-2">
            <v-row class="pt-0" align="start" justify="center" style="background-color:#110b22">
              <v-col cols="12" v-for="article in myArticles" :key="article.id">
                <Post v-bind="article" />
              </v-col>
            </v-row>
          </v-tab-item>
        </v-tabs>
      </v-col>
    </v-row>
  </v-responsive>
</template>

<script>
// import "../../assets/css/components.scss";
// import "../../assets/css/common.scss";
// import "../../assets/css/style.scss";
// import "../../assets/css/user.scss";

import Post from "../../components/common/Post";
import UserApi from "../../apis/UserApi";
import FeedApi from "../../apis/FeedApi";
export default {
  name: "components",
  components: {
    Post
  },
  methods: {
    clickFollowBtn() {
      if (!this.isMyAccount) {
        let { loginedNickname, shownNickname } = this;
        let sendData = { loginedNickname, shownNickname };

        FeedApi.requestFollow(
          sendData,
          res => {
            //성공시
            console.log("성공쿠 : " + res);
            this.isFollow = !this.isFollow;
          },
          error => {
            //실패 시
            console.log("팔로우 실패 ㅜ" + error);
          }
        );
      }
    },
    viewFollows() {
      console.log(this.userInfo.nickname);
      this.$router.push({ name: "팔로", params: this.nickname });
    },
    getLoginUserInformation() {
      if (sessionStorage.getItem("LoginUserInfo")) {
        this.loginedNickname = JSON.parse(
          sessionStorage.getItem("LoginUserInfo")
        ).nickname;
      } else {
        this.$router.push({ name: "Error" });
      }
    },
    getUserInformation() {
      UserApi.requestUserProfile(
        this.$route.params.email,
        res => {
          //확인용 ..useless ...
          let sentData = JSON.stringify(res.data);
          console.log("프로필 정보 : " + JSON.stringify(res.data));
          this.userInfo.followers = JSON.stringify(res.data.followers.length);
          this.userInfo.followings = JSON.stringify(res.data.followings.length);
          this.userInfo.id = res.data.id;
          this.userInfo.intro = res.data.intro;
          this.userInfo.nickname = res.data.nickname;
          this.userInfo.username = res.data.username;
          this.userInfo.picname = require("@/assets/images/profile/" +
            res.data.pic_name +
            ".png");
          this.shownNickname = res.data.nickname;

          if (this.userInfo.nickname === this.loginedNickname) {
            //만약에 지금보는 정보랑 내 로그인 정보가 같으먄
            this.isMyAccount = true;
          } else {
            const followerList = res.data.followers;
            const LoginId = JSON.parse(sessionStorage.getItem("LoginUserInfo"))
              .id;
            // console.log("Login id -> ",LoginId," followerList is -> ",followerList)
            if (followerList.includes(LoginId)) {
              console.log("팔로우한 사람이자너 ~!!");
              this.isFollow = true;
            } else {
              console.log("팔로우 아님 ㅋ");
              this.isFollow = false;
            }

            console.log(followerList);
            this.isMyAccount = false;
            //내 계정이 아니고,
          }
        },
        err => {
          this.$router.push({ path: "/404" });
        }
      )
    },
    getMyArticlesFromServer() {
      this.myArticles=[];

      FeedApi.getMyArticles(
        this.loginedNickname,
        res => {
          console.log("---------------");
          console.log(res.data);
          for (let i = 0; i < res.data.length; i++) {
            let article_prop = {
              nickname: res.data[i].nickname,
              pic_name: require("@/assets/images/profile/" +
                res.data[i].pic_name +
                ".png"),
                img:res.data[i].image,
              id: res.data[i].id,
              article: res.data[i].article,
              hashtags: res.data[i].hashtags,
              likes: JSON.stringify(res.data[i].like_users.length),
              comments: res.data[i].comments,
              created_at: res.data[i].created_at,
            };

            console.log(article_prop);
            this.myArticles.push(article_prop);

          }
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  updated() {
    this.getUserInformation();
    this.getLoginUserInformation();
  },

  created() {
    this.getUserInformation();
    this.getLoginUserInformation();
    this.getMyArticlesFromServer();
  },

  data: () => {
    return {
      loginedNickname: '',
      isFollow: false,
      isMyAccount: false,
      loginUsername: "",
      shownNickname: "",
      userInfo: {
        id: "",
        nickname: "",
        username: "",
        likes: "",
        followers: 0,
        followings: 0,
        picname: "",
        intro: ""
      },
      myArticles: [
        {
          nickname: "",
          picname: "",
          id: 0,
          article: "",
          hashtags: [],
          likes: 0,
          comment: 0,
          time: ""
        }
      ],
      feed: {
        writer: "",
        time: "",
        comments: "",
        isLiked: "",
        isClipped: ""
      },
      text:
        "이곳에 내용이 들어갑니다..... 내용상관없이 모든내용이 나올 예정스 라랄랄"
    };
  },
  computed: {
    setFollowBtn() {
      if (!this.isFollow) {
        return "color : #110b22;";
      } else {
        return "";
      }
    }
  }
};
</script>

