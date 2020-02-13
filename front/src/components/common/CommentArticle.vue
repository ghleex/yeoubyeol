<template>
  <div>
    <v-card class="mx-2" color="#110B22" dark outlined style="border: 1px solid #888">
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
        <p class="mt-1">{{post.article}}</p>
        <v-chip v-for="(tag,i)  in post.hashtags" :key="i" class="ma-1">{{tag}}</v-chip>
      </v-card-text>

      <v-card-actions class="pt-0">
        <v-list-item>
          <v-row class="mr-1" align="center" justify="start">
            <a href="#">
              <v-icon
                class="mr-1"
                size="x-large"
                v-if="!this.post.isLike"
                @click="iLoveIt"
              >mdi-heart-outline</v-icon>
              <v-icon
                class="mr-1"
                size="x-large"
                color="red"
                v-if="this.post.isLike"
                @click="iLoveIt"
              >mdi-heart</v-icon>
              <span class="subheading mr-2" style="color:#ccc">{{this.post.likes}}</span>
            </a>
            <a href="#">
              <v-icon class="mr-1" size="x-large">mdi-comment</v-icon>
              <span class="subheading" style="color:#ccc">{{this.post.comments}}</span>
            </a>
          </v-row>
        </v-list-item>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import FeedApi from "@/apis/FeedApi";
export default {
  name: "CommentArticle",
  props: {
    id: {
      type: Number
    },
    nickname: {
      type: String
    },
    article: {
      type: String
    },
    pic_name: {
      type: String
    },
    hashtags: {
      type: Array
    },
    like_users: {
      type: Array
    },

    likes: {
      type: Number
    },
    comments: {
      type: Number
    },
    created_at: {
      type: String
    }
  },
  data: function() {
    return {
         post:  {
        id: this.id,
        nickname: this.nickname,
        article: this.article,
        
        pic_name: this.pic_name,
        hashtags: this.hashtags,
        like_users: this.like_users,
        likes: this.likes,
        comments: this.comments,
        created_at: this.created_at,
        timedelta: "",
        isLike: false
    },
  }},
  methods: {
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
    isLikeCheck() {
      let LoginId = JSON.parse(sessionStorage.getItem("LoginUserInfo")).id;
      let LoginNickname = JSON.parse(sessionStorage.getItem("LoginUserInfo"))
        .nickname;
      if (this.post.like_users.includes(LoginId)) {
        this.post.isLike = true;
      } else {
        this.post.isLike = false;
      }
    },
    iLoveIt() {
      let LoginId = JSON.parse(sessionStorage.getItem("LoginUserInfo")).id;
      let LoginNickname = JSON.parse(sessionStorage.getItem("LoginUserInfo"))
        .nickname;
      var form = new FormData();
      form.append("article_id", this.post.id);
      form.append("nickname", LoginNickname);
    console.log(this.post.id,'--2',LoginNickname);
      FeedApi.userLikesPost(
        form,
        res => {
          console.log('----',res.data);
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
    }
  },
  created() {
        this.setTimeValues();
    this.isLikeCheck();
  },
 
};
</script>