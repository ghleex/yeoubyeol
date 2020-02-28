<template>
  <v-card dark color="#110b22">
    <v-card-actions class="px-0">
      <v-list-item class="grow px-2 py-0">
        <v-list-item-avatar color="grey darken-3">
          <v-img class="elevation-6" :src="pic_name" />
        </v-list-item-avatar>

        <v-list-item-content @click="gotoUserPfPage(nickname)">
          <v-list-item-title style="color:#71d087">{{nickname}}</v-list-item-title>
          {{intro}}
        </v-list-item-content>
        <v-col align="center" justify="end" cols="4" v-if="!isMyAccount">
          <span class="subheading grey--text px-2">
            <v-btn v-if="!v_isFollowing" text style="color:#71d087" @click="followBtn">FOLLOW</v-btn>
          </span>
        </v-col>
      </v-list-item>
    </v-card-actions>
  </v-card>
</template>

<script>
import FeedApi from "@/apis/FeedApi";

export default {
  // props : ['text', 'image','isLiked','picname'],
  props: {
    id: {
      type: Number
    },
    nickname: {
      type: String
    },
    pic_name: {
      type: String
    },
    intro: {
      type: String
    },
    isFollowing: {
      type: Boolean
    },
    isMyAccount: {
      type: Boolean
    }
  },
  data: function() {
    return {
      loginedNickname:"",
      shownNickname:"",
      v_isFollowing:this.isFollowing
    };
  },
  methods: {
        gotoUserPfPage(id) {
      //페이지 이동을 어떠카지...
      this.$router.push({ name: "프로필", params: { email: id } });
    },
    followBtn() {
      this.shownNickname=this.nickname;
      let userInfo = this.$cookies.get("LoginUserInfo");
       this.loginedNickname = userInfo.nickname;

      let { loginedNickname, shownNickname } = this;
      let sendData = { loginedNickname, shownNickname };
      FeedApi.requestFollow(
        sendData,
        res => {
          //성공시
          this.v_isFollowing=true;
        },
        error => {
          //실패 시
        }
      );
    }
  }
};
</script>
