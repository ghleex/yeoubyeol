<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <!-- 글 원문  -->
      <v-col cols="12">
      <Fame v-for="feed in feeds" :key="feed.id" :article="feed.article" :author="feed.author" :hashtags="feed.hashtags"/>
      </v-col>
    </v-row>
  </v-responsive>
</template>

<script>
import Fame from '@/components/common/Fame.vue'
import FeedApi from '@/apis/FeedApi.js'
export default {
    components: {
        Fame
    },
    created() {
        FeedApi.requestFeedOfFame(response => {
            this.feeds = response.data
        }, error => {

        })
    },
    methods: {
        
    },
    data() {
        return {
            feeds: '',    
        }
    }
}
</script>

<style>

</style>