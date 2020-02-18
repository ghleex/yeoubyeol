<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <!-- 글 원문  -->
      <v-col cols="12">
        <v-flex xs12 sm12 v-for="(items,i) in notifications" :key="i">
          <NotiList v-bind="items" />
        </v-flex>
      </v-col>
    </v-row>
  </v-responsive>
</template>

<script>
import NotiList from "@/components/common/NotiList";
import UserApi from "@/apis/UserApi";

export default {
  components: {
    NotiList
  },
  methods: {
    loadNotifications() {
      let userInfo = this.$cookies.get("LoginUserInfo");
      let loginedNickname = userInfo.nickname;
      UserApi.loadNotifications(loginedNickname, res => {
        console.log(res);
        this.notifications=[];
        for(let i=0; i<res.data.length; i++){
          let noti = {
            is_read:res.data[0][i].is_read,
            created_at:res.data[0][i].created_at,
            message:res.data[0][i].message,
            nickname:res.data[0][i].send_user,
            pic_name:res.data[1][i],
          }
          this.notifications.push(noti);
        }
      },
      error=>{

      });
    }
  },
  created() {
    this.loadNotifications();
  },
  data: () => ({
    //code
    // 1:댓글 2:좋아요 3: (나에게)팔로잉신청 4 (나의)팔로잉거절 5 팔로잉수락
    notifications: [
      {
        uid: "sun_hangbok",
        picName: "default",
        code: "1",
        time: "12:01",
        isRead: false
      },
      {
        uid: "roadhyun",
        picName: "default",
        code: "2",
        time: "10:58",
        isRead: false
      },
      {
        uid: "kkyukkyuhong",
        picName: "default",
        code: "3",
        time: "09:36",
        isRead: false
      },
      {
        uid: "hongjuzzang",
        picName: "default",
        code: "4",
        time: "08:27",
        isRead: false
      },
      {
        uid: "zzidorii",
        picName: "default",
        code: "5",
        time: "07:27",
        isRead: false
      }
    ]
  })
};
</script>

