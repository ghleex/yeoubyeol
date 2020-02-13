<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <v-col cols="12" v-for="arti in articles" :key="arti.id">
        <Post v-bind="arti" />
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
import dotenv from 'dotenv';

dotenv.config();

export default {
  components: {
    Post,
    InfiniteLoading,
  },
  methods: {
   
    infiniteHandler($state) {
      let requireData = new FormData();
      requireData.append('hashtag', this.hashtag)
      requireData.append('start', this.limit)
      axios.post(`http://${process.env.VUE_APP_IP}/articles/hashtag/`, requireData) //api에 url 삽입
      
        .then(response => {
          console.log(response);
          setTimeout(() => { //스크롤 페이징을 띄우기 위한 시간 지연(1초)
            if (response.data.length) {
              for (let i = 0; i < response.data.length; i++) {
                  let article_prop = {
                    nickname: response.data[i].user.nickname,
                    pic_name: require("@/assets/images/profile/" + response.data[i].user.pic_name + ".png"),
                    img:response.data[i].image,
                    id: response.data[i].id,
                    article: response.data[i].article,
                    hashtags: response.data[i].hashtags,
                    likes: response.data[i].like_users.length,
                    comments: response.data[i].comments.length,
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
    this.hashtag=this.$route.params.keyword;
  },
  data: () => {
    return {
      limit: 0,
      articles: [],
      hashtag: '',
    };
  }
};
</script>
