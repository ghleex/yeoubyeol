<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <v-col cols="12" v-for="arti in articles" :key="arti.id">
        <Post v-bind="arti" />
      </v-col>
    </v-row>
    <infinite-loading @infinite="infiniteHandler" spinner="spiral">
      <div slot="no-more" class="grey--text">
        <h3><br/>더이상 새로운 피드가 없어요</h3>
      </div>
      <div slot="no-results" class="grey--text">
        <h3><br/>불러올 피드가 없어요. 친구를 만들어보세요 !</h3>
      </div>
    </infinite-loading>
  </v-responsive>
</template>

<script>
import Post from "@/components/common/Post";
import FeedApi from "@/apis/FeedApi";
import InfiniteLoading from "vue-infinite-loading";
import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

export default {
  components: {
    Post,
    InfiniteLoading
  },
  methods: {
    getUserInformation() {
      if (this.$cookies.isKey("LoginUserInfo")) {
        let userInfo = this.$cookies.get("LoginUserInfo");
        this.loginedNickname = userInfo.nickname;
      } else {
        this.$router.push({ name: "Error" });
      }
    },
    infiniteHandler($state) {
      let requireData = new FormData();
      requireData.append("nickname", this.loginedNickname);
      requireData.append("start", this.limit);
      axios
        .post(`${process.env.VUE_APP_IP}/articles/mainfeed/`, requireData) //api에 url 삽입
        .then(response => {
          setTimeout(() => {
            //스크롤 페이징을 띄우기 위한 시간 지연(1초)
            if (response.data.length) {
              for (let i = 0; i < response.data.length; i++) {
                let article_prop = {
                  nickname: response.data[i].nickname,
                  pic_name: `${process.env.VUE_APP_IP}${response.data[i].pic_name}`,
                  img: response.data[i].image,
                  id: response.data[i].id,
                  article: response.data[i].article,
                  hashtags: response.data[i].hashtags,
                  likes: response.data[i].like_users.length,
                  comments: response.data[i].comments,
                  created_at: response.data[i].created_at,
                  like_users: response.data[i].like_users
                };

                this.articles.push(article_prop);
              }
              // this.articles = this.articles.concat(response.data);
              $state.loaded(); //데이터 로딩
              this.limit += 10;
              if (this.articles.length / 10 == 0) {
                $state.complete(); //데이터가 없으면 로딩 끝
              }
            } else {
              $state.complete();
            }
          }, 1000);
        })
        .catch(error => {});
    }
  },
  created() {
    this.getUserInformation();
  },
  data: () => {
    return {
      limit: 0,
      articles: [],
      loginedNickname: ""
    };
  }
};
</script>
