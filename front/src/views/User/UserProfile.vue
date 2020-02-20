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
            <v-list-item-content class="d-flex justify-center text-center">
              <h3>{{userInfo.likes}}</h3>
              <v-spacer></v-spacer>
              좋아요
            </v-list-item-content>
            <v-list-item-content @click="viewFollows()" class="d-flex justify-center text-center">
              <h3>{{userInfo.followers}}</h3>
              <v-spacer></v-spacer>팔로워
            </v-list-item-content>

            <v-list-item-content @click="viewFollows()" class="d-flex justify-center text-center">
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
            >{{isFollow? "언팔로우" : "팔로우"}}</v-btn>
            <v-btn v-else min-width="190" small color="#71d087" outlined @click="changeView('프로필 변경')">SETTING PROFILE</v-btn>
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
      <keep-alive>


        <v-tabs centered fixed dark background-color="transparent">
          <v-tabs-slider color="#71d087"></v-tabs-slider>

          <v-tab href="#tab-1">
            게시한 피드
            <br />
            {{PostArticle.length}}
          </v-tab>

          <v-tab href="#tab-2">
            좋아한 피드
            <br />
            {{LikeArticle.length}}
          </v-tab>

          <v-tab-item id="tab-1">
            <v-row
              class="pt-0"
              align="start"
              v-if="PostArticle.length>0"
              justify="center"
              style="background-color:#110b22"
            >
              <v-col cols="12" v-for="(article,i) in PostArticle" :key="i">
               <Post v-bind="article" v-on:delPost="delPost" v-on:editPost="editPost" />
              </v-col>
            </v-row>
            <v-row
              class="pt-0"
              align="start"
              v-else
              justify="center"
              style="background-color:#110b22"
            >
              <v-col cols="12" style="border:2px solid #110b22">
                <h3 class="white--text px-3">
                  게시피드가 없어요
                  </h3>
              </v-col>
            </v-row>
          </v-tab-item>

          <v-tab-item id="tab-2">
            <v-row
              class="pt-0"
              align="start"
              v-if="LikeArticle.length>0"
              justify="center"
              style="background-color:#110b22"
            >
              <v-col cols="12" v-for="(article,i) in LikeArticle" :key="i">
                <Post v-bind="article" v-on:delPost="delPost" v-on:editPost="editPost" />
              </v-col>
            </v-row>
            <v-row
              class="pt-0"
              align="start"
              v-else
              justify="center"
              style="background-color:#110b22"
            >
              <v-col cols="12">
                  <h3 class="white--text px-3">

                  좋아한피드가 없어요
                  </h3>
              </v-col>
            </v-row>
          </v-tab-item>
        </v-tabs>
              </keep-alive>
      </v-col>
    </v-row>
  </v-responsive>
</template>

<script>
import Post from "../../components/common/Post";
import UserApi from "../../apis/UserApi";
import FeedApi from "../../apis/FeedApi";
import dotenv from "dotenv";

dotenv.config();
export default {
  name: "components",
  components: {
    Post
  },
  methods: {
    changeView(path) {
      this.pageTitle = path;
      this.$router.push({ name: path });
    },
    editPost(postId) {
      this.$router.push({ name: "피드 수정", params: { postId: postId } });
    },
    delPost(postId) {
      FeedApi.deletePost(
        postId,
        res => {
          //뒤로 가기
          alert("게시글 삭제 완료 ~!!! 나의 감성 안뇽");
          this.getMyArticlesFromServer();
        },
        error => {
          alert("피드 삭제에 오류가 발생했어요 ..");
        }
      );
    },
    clickFollowBtn() {
      if (!this.isMyAccount) {
        let { loginedNickname, shownNickname } = this;
        let sendData = { loginedNickname, shownNickname };

        FeedApi.requestFollow(
          sendData,
          res => {
            //성공시
            this.isFollow = !this.isFollow;
          },
          error => {
            //실패 시
          }
        );
      }
    },
    viewFollows() {
      this.$router.push({ name: "팔로", params: this.nickname });
    },
    getLoginUserInformation() {
      if (this.$cookies.isKey('LoginUserInfo')) {
        let userInfo= this.$cookies.get('LoginUserInfo');
        this.loginedNickname = userInfo.nickname;
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
          this.userInfo.followers = JSON.stringify(res.data.followers.length);
          this.userInfo.followings = JSON.stringify(res.data.followings.length);
          this.userInfo.id = res.data.id;
          this.userInfo.intro = res.data.intro;
          this.userInfo.nickname = res.data.nickname;
          this.userInfo.username = res.data.username;
          /* this.userInfo.picname = require("@/assets/images/profile/" +
            res.data.pic_name +
            ".png"); */
             this.userInfo.picname=`${process.env.VUE_APP_IP}${res.data.pic_name}`;
      
          this.userInfo.likes = res.data.like_nums;
          // this.userInfo.likes = 0;
          this.shownNickname = res.data.nickname;

          if (this.userInfo.nickname === this.loginedNickname) {
            //만약에 지금보는 정보랑 내 로그인 정보가 같으먄
            this.isMyAccount = true;
          } else {
            let userInfo = this.$cookies.get('LoginUserInfo');
            const followerList = res.data.followers;
            const LoginId = userInfo.id;
            if (followerList.includes(LoginId)) {
              this.isFollow = true;
            } else {
              this.isFollow = false;
            }

            this.isMyAccount = false;
            //내 계정이 아니고,
          }
        },
        err => {
          this.$router.push({ path: "/404" });
        }
      );
    },
      /*    pic_name: require("@/assets/images/profile/" +
           dataList[i].pic_name +
           ".png"), */
    getDataFromResponse(dataList, target) {
      for (let i = 0; i < dataList.length; i++) {
        let article_prop = {
          nickname: dataList[i].nickname,
            pic_name:`${process.env.VUE_APP_IP}${dataList[i].pic_name}`,
      
          img: dataList[i].image,
          id: dataList[i].id,
          article: dataList[i].article,
          author:dataList[i].author,
          hashtags: dataList[i].hashtags,
          likes: dataList[i].like_users.length,
          comments: dataList[i].comments,
          created_at: dataList[i].created_at,
          like_users: dataList[i].like_users
        };

        target.push(article_prop);
      }
    },

    getMyArticlesFromServer() {
      this.PostArticle = [];
      this.LikeArticle = [];

      FeedApi.getPostLikedArticles(
        this.$route.params.email,
        res => {
          //게시피드
          this.getDataFromResponse(res.data.my_articles, this.PostArticle);
          this.getDataFromResponse(res.data.like_articles, this.LikeArticle);
        },
        error => {
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
      loginedNickname: "",
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
      PostArticle: [
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
      LikeArticle: [
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
      }
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

