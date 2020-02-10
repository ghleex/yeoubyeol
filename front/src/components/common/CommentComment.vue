<template>
  <v-card class="mx-2 py-0" color="#110B22" dark>
    <v-list-item>
      <v-list-item-avatar color="grey darken-3" size="36">
        <v-img :src="pic_name"></v-img>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title class="subtitle-2">{{nickname}}</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-card-text>{{content}}</v-card-text>

    <v-card-actions>
      <v-btn v-show="isMyComment">Edit</v-btn>
      <v-btn v-show="isMyComment" @click="removeComment">Remove</v-btn>
      <v-spacer></v-spacer>
      {{created_at}}
    </v-card-actions>
  </v-card>

  <!-- <v-card class="mx-2 py-0" color="#110B22" dark outlined style="border: 1px solid #110b22;">
      <v-list>
        <v-list-item-avatar color="grey darken-3" size="36">
          <v-img :src="pic_name"></v-img>
        </v-list-item-avatar>
              {{nickname}}  
        <v-list-item>

                   <p style="color:#ccc">
                     {{content}}
                     </p>
        </v-list-item>
      </v-list>
  </v-card>-->
</template>


<script>
import axios from "axios";
export default {
  name: "CommentComment",
  props: {
    nickname: {
      type: String
    },
    content: {
      type: String
    },
    pic_name: {
      type: String
    },
    created_at: {
      type: String
    }
  },
  data: function() {
    return {
      isMyComment: false
    };
  },
  methods: {
    removeComment() {
      var txt;
      var r = confirm("Press a button!");
      if (r == true) {
        txt = "You pressed OK!";
      } else {
        txt = "You pressed Cancel!";
      }
      console.log(txt);
    }
  },
  created() {
    const LoginNickname = JSON.parse(sessionStorage.getItem("LoginUserInfo"))
      .nickname;
    if (this.nickname === LoginNickname) {
      this.isMyComment = true;
    } else {
      this.isMyComment = false;
    }
  }
};
</script>