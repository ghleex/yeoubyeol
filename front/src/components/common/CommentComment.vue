<template>
  <div>
    <!-- 일반 보여주기 -->
    <v-card class="mx-2 py-0" color="#110B22" dark v-if="!isEdit">
      <v-list-item>
        <v-list-item-avatar color="grey darken-3" size="36" @click="viewUserPfPage(nickname)">
          <v-img :src="pic_name"></v-img>
        </v-list-item-avatar>
        <v-list-item-content @click="viewUserPfPage(nickname)">
          <v-list-item-title class="subtitle-1">{{nickname}}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-card-text class="white--text">{{content}}</v-card-text>

      <v-card-actions class="overline font-weight-thin">
        <div v-show="isMyComment">
          <v-btn small text style="color:#ccc;" @click="editCommentBtn">수정</v-btn>
          <v-btn small text style="color:#ccc;" @click="removeCommentBtn">삭제</v-btn>
        </div>
        <v-spacer></v-spacer>
        {{timedelta}}
      </v-card-actions>
    </v-card>
    <!-- 수정모드 -->
    <v-card class="mx-2 py-0" color="#110B22" dark v-else>
      <v-list-item>
        <v-list-item-avatar color="grey darken-3" size="36">
          <v-img :src="pic_name"></v-img>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title class="subtitle-2">{{nickname}}</v-list-item-title>
        </v-list-item-content>

        <v-btn outlined style="color:#71d087" @keyup.enter="editComment" @click="editComment">수정</v-btn>
      </v-list-item>
      <v-card-actions class="subtitle-2 grey--text text--lighten-5" align="start">
        <v-text-field v-model="secondaryContent" counter="200" label="댓글" filled rounded dense></v-text-field>
      </v-card-actions>
    </v-card>
  </div>
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
    },
    comment_id: {
      type: Number
    }
  },
  data: function() {
    return {
      isEdit: false,
      isMyComment: false,
      secondaryContent: "",
      timedelta: ""
    };
  },
  methods: {
    viewUserPfPage(nickname){
 this.$router.push({ name: "프로필", params: { email: nickname } });
    
    },
    setTimeValues() {
      let date = new Date();
      let maybe = new Date(this.created_at);
      let Hours = Math.ceil((date.getTime() - maybe.getTime()) / 1000 / 60 / 60);
      let Mins = Math.ceil((date.getTime() - maybe.getTime()) / 1000 / 60);
      if (Hours <= 1) {
        this.timedelta = `${Mins}분 전`;
      } else if (Hours < 24) {
        this.timedelta = `${Hours}시간 전`;
      } else {
      let days = Math.ceil((date.getTime()-maybe.getTime()) / 1000 / 60 / 60 / 24);
        this.timedelta = `${days}일 전`;
      }
    },
    editComment() {
      if (this.secondaryContent.trim() === "") {
        alert("내용을 입력해주세요 ");
      } else {
        let data = {"comment_id": this.comment_id, "comment":this.secondaryContent};
        this.$emit("editComment", data);
        this.isEdit = false;
      }
    },
    removeCommentBtn() {
      let ans = confirm("댓글을 삭제할까요 ?");
      if (ans == true) {
        this.$emit("removeComment", this.comment_id);
      } 
    },
    editCommentBtn() {
      // this.$emit('editComment');
      this.isEdit = true;
      this.secondaryContent = this.content;
    }
  },
  created() {
    this.setTimeValues();
    let userInfo = this.$cookies.get('LoginUserInfo');
    const LoginNickname = userInfo.nickname;
    if (this.nickname === LoginNickname) {
      this.isMyComment = true;
    } else {
      this.isMyComment = false;
    }
  }
};
</script>