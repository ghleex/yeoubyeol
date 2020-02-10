<template>
  <div>
    <v-card class="mx-2" color="#110B22" dark outlined style="border: 1px solid #888">
      <v-list-item>
        <v-list-item-avatar color="grey darken-3">
          <v-img :src="pic_name"></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>{{ nickname }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-card-text class="subtitle-2 grey--text text--lighten-5 pb-0">
        {{article}}
        <br />
        <v-row class="overline font-weight-thin pr-4" align="center" justify="end">2시간 전</v-row>
      </v-card-text>

      <v-card-actions class="pt-0">
        <v-list-item>
          <v-row class="mr-1" align="center" justify="end">
            <a href="#">
              <v-icon class="mr-1" size="x-large" v-if="!isLike">mdi-heart-outline</v-icon>
              <v-icon class="mr-1" size="x-large" color="red" v-if="isLike">mdi-heart</v-icon>
              <span class="subheading mr-2"  style="color:#ccc">{{cnt_likes}}</span>
            </a>
            <a href="#">
              <v-icon class="mr-1" size="x-large">mdi-comment</v-icon>
              <span class="subheading" style="color:#ccc">{{cnt_comments}}</span>
            </a>
          </v-row>
        </v-list-item>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "CommentArticle",
  props: {
    id: {
      type: Number,
    },
    nickname: {
      type: String
    },
    article: {
      type: String
    },
    pic_name: {
      type: String
    },
    hashtags: {
      type: Array
    },
    like_users: {
      type: Array
    },
   
    cnt_likes: {
      type: Number
    },
    cnt_comments: {
      type: Number
    },
    created_at: {
      type: String
    }
  },
  data: function() {
    return {
      isLike: false
    };
  },
  methods: {}
};
</script>