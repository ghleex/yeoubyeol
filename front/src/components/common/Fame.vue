<template>
  <v-card dark color="#110B22" outlined style="border: 1px solid #71d087;" class="pt-0">
    <v-card-subtitle class="ma-2 d-flex align-center">
      <v-avatar class="mr-3" size="40">
        <v-img :src="avatar_img"></v-img>
      </v-avatar>
      <span class="subtitle-1">
        유저명 : {{ author }}
      </span>
    </v-card-subtitle>
    <v-card-text class="d-flex justify-center ma-2">
      {{ article }}
    </v-card-text>
    <v-divider dark class="mx-4"></v-divider>
    <v-card-actions class="ma-2">
      <v-chip v-for="hashtag in hashtags" :key="hashtag" label color="#71d087" small class="mx-1">#{{ hashtag }}</v-chip>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
    name: 'fame',
    props: {
      article: {
        type: String,
      },
      author: {
        type: Number,
      },
      hashtags: {
        type: Array,
      },
    },
    data() {
      return {
        avatar_img: require("@/assets/images/profile/" + this.author + ".png")
      }
    }
}
</script>

<style>

</style>