<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <v-col cols="12" v-for="arti in articles" :key="arti.article">
        <Post v-bind="arti" />
      </v-col>
    </v-row>
  </v-responsive>
</template>

<script>
import Post from "@/components/common/Post";
import FeedApi from "@/apis/FeedApi";

export default {
  components: {
    Post
  },
  methods: {
    getUserInformation() {
      if (sessionStorage.getItem("LoginUserInfo")) {
        this.loginedNickname = JSON.parse(
          sessionStorage.getItem("LoginUserInfo")
        ).nickname;
      } else {
        this.$router.push({ name: "Error" });
      }
    },
    getArticlesFromServer() {
      this.articles=[];

      FeedApi.getArticles(
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
              likes: res.data[i].like_users.length,
              comments: res.data[i].comments,
              created_at: res.data[i].created_at,
            };

            console.log(article_prop);
            this.articles.push(article_prop);

          }
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  created() {
    this.getUserInformation();
    this.getArticlesFromServer();
  },
  data: () => {
    return {
      articles: [
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
      loginedNickname: ""
    };
  }
};
</script>
