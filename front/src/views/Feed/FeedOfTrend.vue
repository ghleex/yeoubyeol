<template>
  <v-container>
      <!-- 가장 많이 사용된 태그, 좋아요가 많은 글 -->
      <Post />
  </v-container>
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