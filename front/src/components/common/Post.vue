<template>
  <div>
    <v-card class="mx-2" color="#110B22" dark outlined style="border: 1px solid #71d087;">
      <v-list-item>
        <v-list-item-avatar color="grey darken-3">
          <v-img :src="pic_name"></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>{{ nickname }}</v-list-item-title>
        </v-list-item-content>
        <v-spacer></v-spacer>
        <p class="overline font-weight-thin">{{timedelta}}</p>
      </v-list-item>
      <v-card-text class="subtitle-2 grey--text text--lighten-5 pb-0">
        <v-img :src="getImageUrl"></v-img>
        <p class="mt-1">{{article}}</p>
        <v-chip v-for="(tag,i)  in hashtags" :key="i" class="ma-1">{{tag}}</v-chip>
      </v-card-text>

      <v-card-actions class="pt-0">
        <v-list-item>
          <v-row class="mr-1" align="center" justify="start">
            <a href="#" @click.prevent="iLoveIt">
              <v-icon class="mr-1" size="x-large" v-if="!isLike">mdi-heart-outline</v-icon>
              <v-icon class="mr-1" size="x-large" color="red" v-if="isLike">mdi-heart</v-icon>
              <span class="subheading mr-2 white--text">{{likes}}</span>
            </a>
            <a href="#" @click.prevent="comment">
              <v-icon class="mr-1" size="x-large">mdi-comment-outline</v-icon>
              <span class="subheading white--text">{{comments}}</span>
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

dotenv.config();
export default {
  name: "Post",
  props: {
    keyIdx:{
      type:Number
    },
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
      show: false,
      isLike: false,
      timedelta: ""
    };
  },
  created(){
    this.setTimeValues();
    this.isLikeCheck();

  },
  updated() {
    console.log("post updaated ~~~~");
    this.setTimeValues();
    this.isLikeCheck();
  },
  computed: {
    getImageUrl: function() {
      return `http://${process.env.VUE_APP_IP}${this.img}`;
    }
  },
  methods: {
    isLikeCheck() {
      const LoginId = JSON.parse(sessionStorage.getItem("LoginUserInfo")).id;
      if (this.like_users.includes(LoginId)) {
        this.isLike = true;
      } else {
        this.isLike = false;
      }
    },
    setTimeValues() {
      let date = new Date();
      let maybe = new Date(this.created_at);
      let Hours = Math.ceil((date - maybe) / 1000 / 60 / 60);
      let Mins = Math.ceil((date - maybe) / 1000 / 60);

      if (Hours <= 1) {
        this.timedelta = `${Mins}분 전`;
      } else if (Hours < 24) {
        this.timedelta = `${Hours}시간 전`;
      } else {
        this.timedelta = `${date.getDate() - maybe.getDate()}일 전`;
      }
    },
    iLoveIt() {
      var userinfo = JSON.parse(sessionStorage.getItem("LoginUserInfo"))
        .nickname;
      var form = new FormData();
      form.append("article_id", this.id);
      form.append("nickname", userinfo);
      this.$emit("userLikes",[form,this.keyIdx,this.isLike]);
      
    },
    comment() {
      var router = this.$router;
      // router.push(`feed/${this.id}`);
      this.$router.push({ name: "댓글", params: { id: this.id } });
    }
  }
};
</script>