<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <!-- 글 원문  -->
      <v-col cols="12">
        <div style="text-align:center" class="mt-2">
          <h3 class="white--text">⭐️ 명예의 전당 ⭐️</h3>
          <br />
          <h5 class="white--text">
            명예의 전당은
            <b>5 개 이상의 좋아요</b> 수를 받은 게시글로 선정됩니다.
          </h5>
        </div>
      </v-col>
      <!--  <v-col cols="12" v-for="(feed,idx) in feeds" :key="idx" >
        <Fame v-bind="feed" />
      </v-col>-->
      <v-col cols="12" v-if="isLoading">
        <v-card flat tile dark color="#110B22">
          <v-window v-model="onboarding">
            <v-window-item v-for="(feed,idx) in feeds" :key="idx" class="ma-1">
              <Fame v-bind="feed" />
            </v-window-item>
          </v-window>

          <v-card-actions class="justify-space-between">
            <v-btn text @click="prev">
              <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
            <v-item-group v-model="onboarding" class="text-center" mandatory>
              <v-item
                v-for="n in feeds.length"
                :key="`btn-${n}`"
                v-slot:default="{ active, toggle }"
              >
                <v-btn :input-value="active" icon @click="toggle">
                  <v-icon>mdi-record</v-icon>
                </v-btn>
              </v-item>
            </v-item-group>
            <v-btn text @click="next">
              <v-icon>mdi-chevron-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-responsive>
</template>

<script>
import Fame from "@/components/common/Fame.vue";
import TrendFameApi from "@/apis/TrendFameApi.js";
export default {
  components: { Fame },
  created() {
    TrendFameApi.requestFeedOfFame(
      response => {
        console.log(response);
        this.feeds = [];
        for (let i = 0; i < response.data.length; i++) {
          let feed = {
            id: response.data[i].id,
            article: response.data[i].article,
            hashtags: response.data[i].hashtags,
            image: response.data[i].image
          };
          this.feeds.push(feed);
          this.length = this.feeds.length;
          this.onboarding = 0;
        }
        this.isLoading=true;
      },
      error => {
        alert("게시물을 불러오는데 오류가 발생했어요 ..");
        this.isLoading=false;
      }
    );
  },
  methods: {
    next() {
      this.onboarding =
        this.onboarding + 1 === this.length ? 0 : this.onboarding + 1;
    },
    prev() {
      this.onboarding =
        this.onboarding - 1 < 0 ? this.length - 1 : this.onboarding - 1;
    }
  },
  data() {
    return {
      isLoading:false,
      length: 3,
      onboarding: 0,
      feeds: [
        {
          nickname: "KIKI",
          id: 0,
          article: "testing",
          author: 2,
          hashtags: ["kiki", "hello"]
        }
      ]
    };
  }
};
</script>

<style>
</style>