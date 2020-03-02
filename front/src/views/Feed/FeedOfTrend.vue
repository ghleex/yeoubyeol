<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <!-- 글 원문  -->
      <v-col cols="12">
        <keep-alive>
          <v-tabs centered fixed dark background-color="transparent">
            <v-tabs-slider color="#71d087"></v-tabs-slider>

            <v-tab href="#tab-1">
              지난달의 인기글
              <br />
            </v-tab>

            <v-tab href="#tab-2">
              해쉬태그 추천
              <br />
            </v-tab>

            <v-tab-item id="tab-1">
              <v-row class="pt-0" align="start" justify="center" style="background-color:#110b22" v-if="isLoading">
                <v-col cols="12">
                  <div style="text-align:center" class="mt-2">
                    <h3 class="white--text">지난 달의 인기글이에요</h3>
                    <br />
                    <h5 class="white--text">
                      인기글은 지난달에 가장
                      <b>많은 좋아요</b> 수를 받은 게시글로 선정됩니다.
                    </h5>
                  </div>
                </v-col>
                <v-col cols="12" v-for="(trend,idx) in trends" :key="idx">
                  <h5 class="white--text ml-2">{{idx+1}}위 / 지난달 좋아요 수 : {{trend.last_popular_post}} ❤️</h5>
                  <Post v-bind="trend" />
                </v-col>
              </v-row>
            </v-tab-item>

            <v-tab-item id="tab-2">
              <v-row class="pt-0" align="start" justify="center" style="background-color:#110b22">
                <wordcloud
                  :data="defaultWords"
                  nameKey="name"
                  valueKey="value"
                  color="Accent"
                  spiral="rectangular"
                  :showTooltip="false"
                  :wordClick="wordClickHandler"
                ></wordcloud>
              </v-row>
            </v-tab-item>
          </v-tabs>
        </keep-alive>
      </v-col>
    </v-row>
  </v-responsive>
</template>

<script>
import TrendFameApi from "@/apis/TrendFameApi";
import Post from "@/components/common/Post.vue";
import wordcloud from "vue-wordcloud";
export default {
  components: {
    Post,
    wordcloud
  },
  data: () => ({
    isLoading:false,
    trends: [
    
    ],
    defaultWords: [{ name: "loading", value: 30 }]
  }),
  methods: {
    wordClickHandler(name, value, vm) {
      this.$router.push({ name: "검색 결과", params: { keyword: name } });
    },
    getTrendHashtags() {
      TrendFameApi.requestTrendHashtags(
        0,
        res => {
          this.defaultWords = [];
          for (let i = 0; i < res.data.length; i++) {
            if (res.data[i][0] !== 0) {
              let tag = {
                value: res.data[i][0],
                name: res.data[i][1]
              };
              this.defaultWords.push(tag);
            }
          }
        },
        error => {
          alert("인기있는 해쉬태그를 불러오는데 실패했어요..");
        }
      );
    },
    getTrendArticle() {
      TrendFameApi.requestTrendArticle(
        0,
        response => {
          this.trends = [];
          for (let i = 0; i < response.data.length; i++) {
            let prop = {
              nickname: response.data[i].nickname,
              pic_name: `${process.env.VUE_APP_IP}${response.data[i].pic_name}`,
              img: response.data[i].image,
              id: response.data[i].id,
              article: response.data[i].article,
              hashtags: response.data[i].hashtags,
              likes: response.data[i].like_users.length,
              comments: response.data[i].comments,
              created_at: response.data[i].created_at,
              like_users: response.data[i].like_users,
              popular_post: response.data[i].popular_post,
              last_popular_post: response.data[i].last_popular_post,
            };

            this.trends.push(prop);
          }
        },
        error => {}
      );
    }
  },
  created() {
    this.getTrendHashtags();
    this.getTrendArticle();
    this.isLoading=true;
  }
};
</script>
