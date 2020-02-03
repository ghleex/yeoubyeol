<template>
  <v-tabs centered fixed-tabs dark background-color="transparent"
  class="py-12"
  >
    <v-tabs-slider color="#71d087"></v-tabs-slider>

    <v-tab href="#tab-1">알림</v-tab>

    <v-tab href="#tab-2">요청</v-tab>

    <!-- 알림 탭 부분 -->
    <v-tab-item id="tab-1">
      <v-container v-if="notifications.length>0" centered class="my-0">
        <v-layout row class="my-0 py-0">
          <v-flex xs12 sm12 v-for="(items,i) in notifications" :key="i">
            <NotiList v-bind="items" />
          </v-flex>
        </v-layout>
      </v-container>
      <v-container v-else>
        <p class="white--text subtitle-1">아직 노 알람..Oops!</p>
      </v-container>
    </v-tab-item>
    <!-- 요청 탭 부분 -->
    <v-tab-item id="tab-2">
      <v-container v-if="requests.length>0" centered class="my-0">
        <v-layout row class="my-0 py-0">
          <v-flex xs12 sm12 v-for="(items,i) in requests" :key="i">
            <ReqList v-bind="items" />
          </v-flex>
        </v-layout>
      </v-container>
      <v-container v-else>
        <p class="white--text subtitle-1">아직 노 요청..Oops!</p>
      </v-container>
    </v-tab-item>
  </v-tabs>
</template>

<script>
import NotiList from "../../components/common/NotiList";
import ReqList from "../../components/common/ReqList";

export default {
  components: {
    NotiList,
    ReqList
  },
  data: () => ({
    //code
    // 1:댓글 2:좋아요 3: (나에게)팔로잉신청 4 (나의)팔로잉거절 5 팔로잉수락
    notifications: [
      {
        uid: "sun_hangbok",
        picName: "default",
        code: "1",
        time: "12:01"
      },
      {
        uid: "roadhyun",
        picName: "default",
        code: "2",
        time: "10:58"
      },
      {
        uid: "kkyukkyuhong",
        picName: "default",
        code: "3",
        time: "09:36"
      },
      {
        uid: "hongjuzzang",
        picName: "default",
        code: "4",
        time: "08:27"
      },
      {
        uid: "zzidorii",
        picName: "default",
        code: "5",
        time: "07:27"
      }
    ],
    requests: [
      {
      uid:'zzidorii',
      picName:"default",
      time:"07:29"
    },
      {
      uid:'zzidorii',
      picName:"default",
      time:"07:29"
    },
      {
      uid:'zzidorii',
      picName:"default",
      time:"07:29"
    },
      {
      uid:'zzidorii',
      picName:"default",
      time:"07:29"
    },
      {
      uid:'zzidorii',
      picName:"default",
      time:"07:29"
    },
      {
      uid:'zzidorii',
      picName:"default",
      time:"07:29"
    },
    ]
  })
};
</script>

