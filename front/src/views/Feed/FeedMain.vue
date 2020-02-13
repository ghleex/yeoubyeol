<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <v-col cols="12" v-for="arti in articles" :key="arti.id">
        <Post v-bind="arti"  />
      </v-col>
    </v-row>
    <infinite-loading @infinite="infiniteHandler" spinner="spiral"></infinite-loading>
  </v-responsive>
</template>

<script>
import Post from "@/components/common/Post";
import FeedApi from "@/apis/FeedApi";
import InfiniteLoading from 'vue-infinite-loading';
import axios from 'axios'
import dotenv from "dotenv";

dotenv.config();

export default {
  components: {
    Post,
    InfiniteLoading,
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
    // getArticlesFromServer() {
    //   this.articles=[];

    //   FeedApi.getArticles(
    //     this.loginedNickname,
    //     res => {
    //       for (let i = 0; i < res.data.length; i++) {
    //         let article_prop = {
    //           nickname: res.data[i].nickname,
    //           pic_name: require("@/assets/images/profile/" +
    //             res.data[i].pic_name +
    //             ".png"),
    //             img:res.data[i].image,
    //           id: res.data[i].id,
    //           article: res.data[i].article,
    //           hashtags: res.data[i].hashtags,
    //           likes: res.data[i].like_users.length,
    //           comments: res.data[i].comments,
    //           created_at: res.data[i].created_at,
    //           like_users:res.data[i].like_users,
    //         };

    //         this.articles.push(article_prop);

    //       }
    //     },
    //     error => {
    //       console.log(error);
    //     }
    //   );
    // },
    infiniteHandler($state) {
      let requireData = new FormData();
      requireData.append('nickname', this.loginedNickname)
      requireData.append('start', this.limit)
      axios.post('${process.env.VUE_APP_IP}/articles/mainfeed/', requireData) //api에 url 삽입
        .then(response => {
          setTimeout(() => { //스크롤 페이징을 띄우기 위한 시간 지연(1초)
            if (response.data.length) {
              for (let i = 0; i < response.data.length; i++) {
                  let article_prop = {
                    nickname: response.data[i].nickname,
                    pic_name: require("@/assets/images/profile/" + response.data[i].pic_name + ".png"),
                    img:response.data[i].image,
                    id: response.data[i].id,
                    article: response.data[i].article,
                    hashtags: response.data[i].hashtags,
                    likes: response.data[i].like_users.length,
                    comments: response.data[i].comments,
                    created_at: response.data[i].created_at,
                    like_users:response.data[i].like_users,
                  };

                  this.articles.push(article_prop);
                }
              // this.articles = this.articles.concat(response.data);
              $state.loaded(); //데이터 로딩
              this.limit += 10 
              if (this.articles.length / 10 == 0) {
                $state.complete(); //데이터가 없으면 로딩 끝
              }
            } else {
              $state.complete();
            }
          }, 1000)
        }).catch(error => {
          console.error(error);
        })
    }
  },
  created() {
    this.getUserInformation();
    // this.getArticlesFromServer();
    // let requireData = new FormData();
    // requireData.append('nickname', this.loginedNickname)
    // requireData.append('start', this.limit)
    // axios.post('http://192.168.31.87:8000/articles/mainfeed/', requireData)
    //   .then((response) => {
    //     if (response.data.length) {
    //       for (let i = 0; i < response.data.length; i++) {
    //           let article_prop = {
    //             nickname: response.data[i].nickname,
    //             pic_name: require("@/assets/images/profile/" + response.data[i].pic_name + ".png"),
    //             img:response.data[i].image,
    //             id: response.data[i].id,
    //             article: response.data[i].article,
    //             hashtags: response.data[i].hashtags,
    //             likes: response.data[i].like_users.length,
    //             comments: response.data[i].comments,
    //             created_at: response.data[i].created_at,
    //             like_users:response.data[i].like_users,
    //           };

    //           this.articles.push(article_prop);
    //         }
    //       this.limit += 10
    //     }
    //   })
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
