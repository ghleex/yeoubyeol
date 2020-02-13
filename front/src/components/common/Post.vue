<template>
  <div>
    <v-card class="mx-2" color="#110B22" dark outlined style="border: 1px solid #71d087;">
      <v-list-item>
        <v-list-item-avatar color="grey darken-3">
          <v-img :src="post.pic_name"></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>{{ post.nickname }}</v-list-item-title>
        </v-list-item-content>
        <v-spacer></v-spacer>
        <p class="overline font-weight-thin">{{post.timedelta}}</p>
      </v-list-item>
      <v-card-text class="subtitle-2 grey--text text--lighten-5 pb-0">
        <v-img :src="imgUrl"></v-img>
        <p class="mt-1">{{post.article}}</p>
        <v-chip v-for="(tag,i)  in post.hashtags" :key="i" class="ma-1">{{tag}}</v-chip>
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
    id: {
      type: Number,
      required: true
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
      imgUrl:'',
      post: {
        id: "",
        nickname: '',
        article: '',
        img: "../../assets/images/profile/1.png",
        pic_name: "../../assets/images/profile/1.png",
        comments: 0,
        likes: 0,
        created_at: '',
        hashtags: [],
        like_users: [],
        timedelta: "",
        isLike: false
      }
    };
  },
  created() {
    this.post= {
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
        isLike: false
      },
    this.setTimeValues();
    this.isLikeCheck();
    this.getImageUrl();
  },

  methods: {
      getImageUrl() {
      this.imgUrl= `http://${process.env.VUE_APP_IP}${this.post.img}`;
    },
     isLikeCheck() {
      let userInfo = this.$cookies.get('LoginUserInfo');
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
      let userInfo = this.$cookies.get('LoginUserInfo');
      var form = new FormData();
      let LoginId = userInfo.id;
      let LoginNickname = userInfo.nickname;
      form.append("article_id", this.post.id);
      form.append("nickname", LoginNickname);
 console.log(this.post.id,'--1',LoginNickname);
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
          alert("게시글 좋아요에 문제가 발생했습니다.. 지송");
        }
      );
    },

    comment() {
      var router = this.$router;
      // router.push(`feed/${this.id}`);
      this.$router.push({ name: "댓글", params: { id: this.post.id } });
    }
  }
};
</script>