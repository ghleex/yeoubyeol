<template>
  <div class="py-12">
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
        {{feed.post}}
      </v-tab>
      <v-tab href="#tab-2">
        <v-icon>mdi-lead-pencil</v-icon>
      </v-tab>

      <v-tab href="#tab-3">
        좋아한 피드
        <br />
        {{feed.liked}}
      </v-tab>

      <v-tab-item id="tab-1">
          <Post :content="text" :isLiked="false" :isClipped="true" />
          <Post :content="text" :isLiked="false" :isClipped="true" />
          <Post :content="text" :isLiked="false" :isClipped="true" />
          <Post :content="text" :isLiked="false" :isClipped="true" />
      </v-tab-item>
      <v-tab-item id="tab-2">
        <v-card dark color="#110b22">
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-row class="py-0 ma-2">
              <v-col cols="12" class="pa-1">
                <v-file-input accept="image/*" ></v-file-input>
                <!-- <v-text-field dark label="홍주의 미니랩실" required></v-text-field> -->
              </v-col>

              <v-col cols="12" class="pa-1">
                <v-textarea
                  dark
                  :rules="contentRules"
                  required
                  outlined
                  :value="inputPostContent"
                ></v-textarea>
                <v-btn
                  block
                  class="mb-2"
                  color="#71d087"
                  style="color:#110b22"
                  @click="validate"
                  :disabled="!valid"
                >피드 발행하기</v-btn>
              </v-col>
            </v-row>
          </v-form>
        </v-card>
      </v-tab-item>
      <v-tab-item id="tab-3">
        <v-container>
          <v-btn>click</v-btn>
        </v-container>
      </v-tab-item>
    </v-tabs>
  </div>
</template>

<script>
import "../../assets/css/components.scss";
import "../../assets/css/common.scss";
import "../../assets/css/style.scss";
import "../../assets/css/user.scss";

import Post from "../../components/common/Post";
import UserApi from "../../apis/UserApi";
import FeedApi from "../../apis/FeedApi";

export default {
  name: "components",
  components: {
    Post
  },
  methods: {
    validate() {
      if (this.$refs.form.validate()) {
        // this.snackbar = true;
        this.newPost();
      }
    },
    newPost() {


    let data = new FormData();
    data.append('nickname', this.loginedNickname);
    data.append('article', 'my-picture');
    data.append('image', event.target.files[0]); 

    FeedApi.newPost(data,res=>{

    })

  }
    },
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
  created() {
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
        this.shownNickname = res.data.nickname;
        this.loginedNickname = sessionStorage.getItem("LoginUserNickname");

        if (
          this.userInfo.nickname === sessionStorage.getItem("LoginUserNickname")
        ) {
          //만약에 지금보는 정보랑 내 로그인 정보가 같으먄
          this.isMyAccount = true;
        } else {
          this.isMyAccount = false;
          //내 계정이 아니고,
        }
      },
      error => {
        this.$router.push({ path: "/404" });
      }
    ),
      // (this.userInfo.email = this.$route.params.email),
      (this.userInfo.likes = 1225),
      (this.feed.post = 3452),
      (this.feed.liked = 124),
      (this.feed.keywords = 45),
      (this.userInfo.picname = "default");
  },

  data: () => {
    return {
      inputPostContent:'',
      valid: false,
      contentRules: [v => !!v || "내용을 입력해주세요.."],
      isFollow: false,
      isMyAccount: false,
      loginUsername: "",
      shownUsername: "",
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
      feed: {
        post: "",
        liked: "",
        keywords: "",
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

