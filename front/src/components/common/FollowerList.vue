<template>
  <v-card dark color="#110b22">
    <v-card-actions class="mx-0">
      <v-list-item class="grow px-2 py-0">
        <v-list-item-avatar color="grey darken-3">
          <v-img class="elevation-6" :src="getPic"></v-img>
        </v-list-item-avatar>

        <v-list-item-content @click="changeViewProfile('프로필',shownNickname)">
          <v-list-item-title style="color:#71d087">{{shownNickname}}</v-list-item-title>
          {{intro}}
        </v-list-item-content>

        <v-col align="center" justify="end" cols="4" v-if="isMyAccount">
          <span class="subheading grey--text px-2">
            <!-- <v-btn v-if="isFollowing" text style="color:#71d087" @click="unfollowBtn">UNFOLLOW</v-btn> -->
            <v-btn v-if="!isFollowing" text style="color:#71d087"  @click="followBtn">팔로우</v-btn>
          </span>
        </v-col>
      </v-list-item>
    </v-card-actions>
  </v-card>
</template>

<script>
import FeedApi from "@/apis/FeedApi";
import dotenv from "dotenv";

dotenv.config();
export default {
  props: {
    intro: {
      type: String,
      default: " "
    },
    shownNickname: {
      type: String,
      default: "default"
    },
    picName: {
      type: String,
      default: "0"
    },
    isFollowing: {
      type: Boolean,
      default: false
    },
    isMyAccount: {
      type: Boolean,
      default: false
    }
  },
  data: function() {
    return {
      getPic: `${process.env.VUE_APP_IP}/uploads/accounts/pic_names/1.jpg`,
      loginedNickname: ""
    };
  },
  methods: {
    changeViewProfile(path, usersEmail) {
      this.pageTitle = usersEmail;
      this.$router.push({ name: path, params: { email: usersEmail } });
    },
    followBtn() {
      let { loginedNickname, shownNickname } = this;
      let sendData = { loginedNickname, shownNickname };
      FeedApi.requestFollow(
        sendData,
        res => {
          //성공시
          this.$emit('updateFollowerList');
        },
        error => {
          //실패 시
        }
      );
    }
  },
  created() {
    let userInfo = this.$cookies.get('LoginUserInfo')
    this.loginedNickname = userInfo.nickname;
    // this.getPic = require("@/assets/images/profile/" + this.picName + ".png");
     this.getPic=`${process.env.VUE_APP_IP}${this.picName}`;
      
  }
};
</script>
