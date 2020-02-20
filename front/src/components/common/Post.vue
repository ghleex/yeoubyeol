<template>
  <div>
    <v-card class="mx-2" color="#110B22" dark outlined style="border: 1px solid #ccc;">
      <!-- <v-card class="mx-2" color="#110B22" dark outlined style="border: 1px solid #71d087;"> -->
      <v-list-item>
        <v-list-item-avatar color="grey darken-3">
          <v-img :src="post.pic_name"></v-img>
        </v-list-item-avatar>

        <v-list-item-content @click="viewUserPfPage(post.nickname)">
          <v-list-item-title>{{ post.nickname }}</v-list-item-title>
        </v-list-item-content>
        <v-spacer></v-spacer>
        <p class="overline font-weight-thin">{{post.timedelta}}</p>
      </v-list-item>
      <v-card-text class="subtitle-2 grey--text text--lighten-5 pb-0">
        <v-img :src="imgUrl"></v-img>
        <div style="white-space:pre-wrap;" class="my-2">{{post.article}}</div>
        <v-chip
          v-for="(tag,i)  in post.hashtags"
          :key="i"
          class="ma-1"
          @click="gotoKeywordDetailPage(tag)"
        >{{tag}}</v-chip>
      </v-card-text>

      <v-card-actions class="pt-0">
        <v-list-item>
          <v-row class="mr-1" align="center" justify="start">
            <a href="#" @click.prevent="iLoveIt">
              <v-icon class="mr-1" size="x-large" v-if="!post.isLike">mdi-heart-outline</v-icon>
              <v-icon class="mr-1" size="x-large" color="red" v-if="post.isLike">mdi-heart</v-icon>
              <span class="subheading mr-2 white--text">{{post.likes}}</span>
            </a>
            <a href="#" @click.prevent="comment">
              <v-icon class="mr-1" size="x-large">mdi-comment-outline</v-icon>
              <span class="subheading white--text">{{post.comments}}</span>
            </a>
            <v-spacer></v-spacer>
            <div v-show="isMyPost">
              <v-btn small text style="color:#ccc;" @click="editPostBtn">수정</v-btn>
              <v-btn small text style="color:#ccc;" @click="removePostBtn">삭제</v-btn>
            </div>
          </v-row>
        </v-list-item>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import axios from "axios";
import dotenv from "dotenv";
import FeedApi from "@/apis/FeedApi";

dotenv.config();

export default {
  name: "Post",
  props: {
    author: {
      type: Number
    },
    id: {
      type: Number
    },
    nickname: {
      type: String
    },
    article: {
      type: String
    },
    img: {
      type: String
    },
    pic_name: {
      type: String,
      default: "0"
    },
    comments: {
      type: Number
    },
    likes: {
      type: Number
    },
    created_at: {
      type: String
    },
    hashtags: {
      type: Array
    },
    like_users: {
      type: Array
    }
  },
  data: function() {
    return {
      validButton: "",
      isMyPost: false,
      imgUrl: "",
      post: {
        id: -1,
        nickname: "loading",
        article: "게시글을 불러오는 중이에요",
        img: "/uploads/articles/images/default.jpg",
        pic_name: "../../assets/images/profile/1.png",
        comments: 0,
        likes: 0,
        created_at: "",
        hashtags: [],
        like_users: [],
        timedelta: "",
        author: 0,
        isLike: false
      }
    };
  },
  created() {
    this.post = {
      id: this.id,
      nickname: this.nickname,
      article: this.article,
      img: this.img,
      pic_name: this.pic_name,
      comments: this.comments,
      likes: this.likes,
      created_at: this.created_at,
      hashtags: this.hashtags,
      like_users: this.like_users,
      timedelta: "",
      isLike: false,
      author: this.author
    };
    let user = this.$cookies.get("LoginUserInfo");
    // let LoginId = JSON.parse(sessionStorage.getItem("LoginUserInfo")).id;
    let LoginId = user.id;

    // if(LoginId=== this.post.author && (currHour>=23 && currHour< 6)){
    this.setTimeValues();
    this.validButton = setInterval(() => {
      let date = new Date();
      let currHour = date.getHours();
      if (LoginId === this.post.author && currHour >= 9 && currHour < 17) {
        this.isMyPost = true;
      } else {
        this.isMyPost = false;
      }
    }, 1000);
    this.isLikeCheck();
    this.getImageUrl();
  },
  beforeRouteLeave(to, from, next) {
    clearInterval(this.validButton);
    return next();
  },
  methods: {
    gotoKeywordDetailPage(target) {
      this.$router.push({ name: "검색 결과", params: { keyword: target } });
    },
    viewUserPfPage(usernickname) {
      this.$router.push({ name: "프로필", params: { email: usernickname } });
    },
    editPostBtn() {
      let date = new Date();
      if (date.getHours() >= 9 && date.getHours() < 17) {
        this.$emit("editPost", this.post.id);
      } else {
        alert(
          "지금은 수정이 가능한 시간이 아니에요 . 오전 9시부터 오후 5시까지 가능합니다."
        );
      }
    },
    removePostBtn() {
      let date = new Date();
      let ans = confirm("게시글을 삭제할까요 ?");
      if (ans == true) {
        if (date.getHours() >= 9 && date.getHours() < 17) {
          this.$emit("delPost", this.post.id);
        } else {
          alert(
            "지금은 삭제가 가능한 시간이 아니에요 . 오전 9시부터 오후 5시까지 가능합니다."
          );
        }
      }
    },
    getImageUrl() {
      this.imgUrl = `${process.env.VUE_APP_IP}${this.post.img}`;
    },
    isLikeCheck() {
      let userInfo = this.$cookies.get("LoginUserInfo");
      let LoginId = userInfo.id;
      if (this.post.like_users.includes(LoginId)) {
        this.post.isLike = true;
      } else {
        this.post.isLike = false;
      }
    },
    setTimeValues() {
      let date = new Date();
      let maybe = new Date(this.post.created_at);
      let Hours = Math.ceil((date - maybe) / 1000 / 60 / 60);
      let Mins = Math.ceil((date - maybe) / 1000 / 60);

      if (Hours <= 1) {
        this.post.timedelta = `${Mins}분 전`;
      } else if (Hours < 24) {
        this.post.timedelta = `${Hours}시간 전`;
      } else {
        this.post.timedelta = `${date.getDate() - maybe.getDate()}일 전`;
      }
    },
    iLoveIt() {
      let userInfo = this.$cookies.get("LoginUserInfo");
      let form = new FormData();
      let LoginId = userInfo.id;
      let LoginNickname = userInfo.nickname;
      form.append("article_id", this.post.id);
      form.append("nickname", LoginNickname);
      // this.PostArticle[data[1]].article="SSSSSSs";
      FeedApi.userLikesPost(
        form,
        res => {
          if (res.data.like_users.includes(LoginId)) {
            this.post.isLike = true;
          } else {
            this.post.isLike = false;
          }
          this.post.likes = res.data.like_users.length;
        },
        error => {
          alert(
            "게시글 좋아요에 문제가 발생했습니다. 잠시 후 다시 시도해 주세요."
          );
        }
      );
    },

    comment() {
      let router = this.$router;
      this.$router.push({ name: "댓글", params: { id: this.post.id } });
    }
  }
};
</script>