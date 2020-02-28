<template>
  <v-card dark color="#110B22" outlined style="border: 1px solid #71d087;" class="ma-2">
    <v-img :src="imgUrl"></v-img>

    <v-card-text>
      <div style="white-space:pre-wrap;" class="my-2">{{article}}</div>
    </v-card-text>

    <v-divider class="mx-4"></v-divider>
    <v-card-title class="pa-1 ml-1">
      <v-chip
        v-for="(hashtag,idx) in hashtags"
        :key="idx"
        @click="gotoKeywordDetailPage(hashtag)"
      >{{hashtag}}</v-chip>
    </v-card-title>
  </v-card>
</template>

<script>
import dotenv from "dotenv";

dotenv.config();
export default {
  name: "Fame",
  props: {
    id: {
      type: Number
    },
    article: {
      type: String
    },
    hashtags: {
      type: Array
    },
    image: {
      type: String
    }
  },
  data() {
    return {
      imgUrl: "@/assets/images/default.jpg"
    };
  },
  created() {
    this.imgUrl = `${process.env.VUE_APP_IP}${this.image}`;
  },
  methods: {
    gotoKeywordDetailPage(target) {
      this.$router.push({ name: "검색 결과", params: { keyword: target } });
    }
  }
};
</script>
