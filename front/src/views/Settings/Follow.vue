<template>
  <v-tabs centered fixed-tabs dark background-color="transparent" class="py-12">
    <v-tabs-slider color="#71d087"></v-tabs-slider>

    <v-tab href="#tab-1">잉</v-tab>

    <v-tab href="#tab-2">워</v-tab>

    <!-- 잉~~ 부분 -->
    <v-tab-item id="tab-1">
      <v-container v-if="followings.length>0" centered class="my-0">
        <v-layout row class="my-0 py-0">
          <v-flex xs12 sm12 v-for="(items,i) in followings" :key="i">
            <FollowList v-bind="items" :isFollowing='true'/>
          </v-flex>
        </v-layout>
      </v-container>
      <v-container v-else>
        <p class="white--text subtitle-1">아직 노 팔로잉..Oops! 친구를 팔로잉해봐용</p>
      </v-container>
    </v-tab-item>
    <!-- 워 ~~~ 부분 -->
    <v-tab-item id="tab-2">
      <v-container v-if="followers.length>0" centered class="my-0">
        <v-layout row class="my-0 py-0">
          <v-flex xs12 sm12 v-for="(items,i) in followers" :key="i">
            <FollowList v-bind="items" :isFollowing='false' />
          </v-flex>
        </v-layout>
      </v-container>
      <v-container v-else>
        <p class="white--text subtitle-1">아직 노 팔로우..Oops! 자극적인 글을 써보는건 어떨까요??? </p>
      </v-container>
    </v-tab-item>
  </v-tabs>
</template>

<script>
import FollowList from "../../components/common/FollowList";

export default {
  components: {
    FollowList
  },
  data: () => ({
    //code
    // 1:댓글 2:좋아요 3: (나에게)팔로잉신청 4 (나의)팔로잉거절 5 팔로잉수락
    followings: [
      {
        email: "sun_hangbok",
        nickName: "선행복",
        picName: "default"
      },
      {
        email: "roadhyun",
        nickName: "선행복",
        picName: "default"
      },
      {
        email: "kkyukkyuhong",
        nickName: "선행복",
        picName: "default"
      }
    ],
    followers: [
      {
        email: "zzidorii",
        nickName: "선행복",
        picName: "default"
      },
      {
        email: "zzidorii",
        nickName: "선행복",
        picName: "default"
      },
      {
        email: "zzidorii",
        nickName: "선행복",
        picName: "default"
      },
      {
        email: "zzidorii",
        nickName: "선행복",
        picName: "default"
      }
    ]
  })
};
</script>

