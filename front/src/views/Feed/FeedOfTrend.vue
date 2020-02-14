<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <!-- 글 원문  -->
      <v-col cols="12">
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