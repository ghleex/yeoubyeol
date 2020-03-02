<template>
  <v-card dark :color="getColor" @click="readNotification">
    <v-card-actions class="px-0">
      <div class="px-2 py-0">
        <v-avatar color="grey darken-3" class="mx-1" size="36">
          <v-img class="elevation-6" :src="noti.pic_name"></v-img>
        </v-avatar>
        <span class="caption">{{getMessage}}</span>
      </div>
      <v-spacer></v-spacer>
      <h6 class="grey--text mx-3">{{noti.timedelta}}</h6>
    </v-card-actions>
  </v-card>
</template>

<script>
import dotenv from "dotenv";
import UserApi from "@/apis/UserApi";

dotenv.config();
export default {
  props: {
    id: {
      type: Number
    },
    nickname: {
      type: String
    },
    is_read: {
      type: Boolean
    },
    created_at: {
      type: String
    },
    message: {
      type: String
    },
    article_no: {
      type: Number
    },
    pic_name: {
      type: String
    }
  },
  data: function() {
    return {
      noti: {
        id: -1,
        nickname: "",
        is_read: false,
        created_at: "",
        message: "",
        article_no: null,
        pic_name: require("@/assets/images/profile_default.png"),
        timedelta: ""
      }
    };
  },
  created() {
    this.noti.id = this.id;
    this.noti.nickname = this.nickname;
    this.noti.is_read = this.is_read;
    this.noti.created_at = this.created_at;
    this.noti.message = this.message;
    this.noti.article_no = this.article_no;
    this.noti.pic_name = `${process.env.VUE_APP_IP}${this.pic_name}`;
    this.setTimeValues();
  },
  methods: {
    readNotification() {
      if (!this.noti.is_read) {
        this.noti.is_read = true;
        UserApi.readNotification(
          this.noti.id,
          res => {
            //타입에 따라 페이지 이동
            if (this.noti.message === "MJ") {
              this.$router.push({'name':'명예의 전당'})
            } else if (this.noti.message === "LK") {
              this.$router.push({ name: "댓글", params: { id: this.noti.article_no} });
            } else if (this.noti.message === "CO") {
              this.$router.push({ name: "댓글", params: { id: this.noti.article_no} });
            } else if (this.noti.message === "FL") {
              this.$router.push({ name: "프로필", params: { email: this.noti.nickname } });
            } else {
             alert("등록되지 않은 알림이에요..");
            }
          },
          error => {
            alert("알림에 문제가 생겼어요..");
          }
        );
      }
    },
    setTimeValues() {
      let date = new Date();
      let maybe = new Date(this.noti.created_at);
      let Hours = Math.ceil((date.getTime() - maybe.getTime()) / 1000 / 60 / 60);
      let Mins = Math.ceil((date.getTime() - maybe.getTime()) / 1000 / 60);
      if (Hours <= 1) {
        this.noti.timedelta = `${Mins}분 전`;
      } else if (Hours < 24) {
        this.noti.timedelta = `${Hours}시간 전`;
      } else {
      let days = Math.ceil((date.getTime()-maybe.getTime()) / 1000 / 60 / 60 / 24);
        this.noti.timedelta = `${days}일 전`;
      }
    }
  },
  computed: {
    getColor: function() {
      return this.noti.is_read ? "#110b22" : "#231e32";
    },
    getMessage: function() {
      if (this.noti.message === "MJ") {
        return "회원님의 게시글이 명예의 전당에 게시되었습니다.";
      } else if (this.noti.message === "LK") {
        return `${this.noti.nickname}님이 회원님의 게시글을 좋아합니다.`;
      } else if (this.noti.message === "CO") {
        return `${this.noti.nickname}님이 회원님의 게시글에 댓글을 남겼습니다.`;
      } else if (this.noti.message === "FL") {
        return `${this.noti.nickname}님이 회원님을 팔로우합니다.`;
      } else {
        return `등록되지 않은 알림이에요`;
      }
    }
  }
};
</script>
