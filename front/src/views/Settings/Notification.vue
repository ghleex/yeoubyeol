<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <v-progress-linear :active="loading" :indeterminate="loading" absolute color="green"></v-progress-linear>
      <v-col cols="12" v-if="!loading" class="pt-0">
        <v-btn text block class="red--text" @click="readAll">모두 읽음 처리</v-btn>
      </v-col>
      <!-- 글 원문  -->
      <v-col cols="12" v-if="!loading" class="pt-0">
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
    async readAll() {
      await this.postReadSign();
      this.loadNotifications();
    },
    postReadSign() {
      return new Promise((succ, fail) => {
        this.loading = true;
        console.log("promise ~~~~~~~~~~~");
        for (let i = 0; i < this.notifications.length; i++) {
          if (!this.notifications[i].is_read) {
            let noti_id = this.notifications[i].id;
            UserApi.readNotification(
              noti_id,
              res => {
                succ(res);
              },
              error => {
                fail(error);
              }
            );
          }
        }
      });
    },

    loadNotifications() {
      let userInfo = this.$cookies.get("LoginUserInfo");
      let userId = userInfo.id;
      console.log("load notification ~~");
        this.notifications = [];
      UserApi.loadNotifications(
        userId,
        res => {
          for (let i = 0; i < res.data.noti_ids.length; i++) {
            let noti = {
              id: res.data.noti_ids[i],
              nickname: res.data.send_nicknames[i],
              is_read: res.data.notifications[i].is_read,
              created_at: res.data.notifications[i].created_at,
              message: res.data.notifications[i].message,
              article_no: res.data.notifications[i].article_no,
              pic_name: res.data.pic_names[i]
            };
            this.notifications.push(noti);
          }
          this.loading = false;
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  created() {
    this.loading = true;
    this.loadNotifications();

    this.timeCalc = setInterval(() => {
      this.loadNotifications();
      console.log("yam22");
    }, 5000);
  },
  beforeRouteLeave(to, from, next) {
    clearInterval(this.timeCalc);
    return next();
  },
  data: () => ({
    //code
    timeCalc: "",
    loading: true,
    notifications: []
  })
};
</script>

