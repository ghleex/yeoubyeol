<template>
  <v-card dark color="#1e192b">
    <v-card-actions class="px-0">
      <v-list-item class="grow px-2 py-0">
        <v-list-item-avatar color="grey darken-3">
          <v-img class="elevation-6" :src="noti.pic_name"></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title style="color:#71d087">{{noti.nickname}}</v-list-item-title>
          {{noti.message}}
        </v-list-item-content>

        <v-row align="center" justify="end">
          <span class="subheading grey--text px-2">{{noti.created_at}}</span>
        </v-row>
      </v-list-item>
    </v-card-actions>
  </v-card>
</template>

<script>
import dotenv from "dotenv";

dotenv.config();
export default {
  // props : ['text', 'image','isLiked','picname'],
  props: {
    is_read: {
      type: Boolean
    },
    created_at: {
      type: String
    },
    message: {
      type: String
    },
    nickname: {
      type: String
    },
    pic_name: {
      type: String,
    }
  },
  data: function() {
    return {
      noti: {
        is_read: false,
        created_at: "",
        message: "",
        nickname: "",
        pic_name: require("@/assets/images/profile_default.png")
      }
    };
  },
  created() {
    this.noti.is_read = this.is_read;
    this.noti.created_at = this.created_at;
    this.noti.message = this.message;
    this.noti.nickname = this.nickname;
    this.noti.pic_name = `${process.env.VUE_APP_IP}${this.pic_name}`;
  },
  
};
</script>
