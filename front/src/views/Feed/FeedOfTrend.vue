<template>
<<<<<<< HEAD
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <!-- 글 원문  -->
      <v-col cols="12">
=======
  <v-container>
      <!-- 가장 많이 사용된 태그, 좋아요가 많은 글 -->
>>>>>>> 22c8c236438b7ed14c9ee15904bea34bc45aeb4e
      <Post />
      </v-col>
    </v-row>
  </v-responsive>
</template>

<script>
import Post from '@/components/common/Post.vue'
export default {
    components: {
        Post
    }
}
</script>

<style>

</style>