<template>
  <v-tabs centered fixed-tabs dark background-color="transparent" class="py-12">
    <v-tabs-slider color="#71d087"></v-tabs-slider>

    <v-tab href="#tab-1">워</v-tab>

    <v-tab href="#tab-2">잉</v-tab>

    <!-- 워 ~~~ 부분 -->
    <v-tab-item id="tab-1">
      <v-container v-if="followers.length>0" centered class="my-0">
        <v-layout row class="my-0 py-0">
          <v-flex xs12 sm12 v-for="(items,i) in followers" :key="i">
            <FollowerList v-bind="items" :isFollowing="true" :isMyAccount="isMyAccount" />
          </v-flex>
        </v-layout>
      </v-container>
      <v-container v-else>
        <p class="white--text subtitle-1">아직 노 팔로워..Oops! 자극적인 글을 써보는건 어떨까요???</p>
      </v-container>
    </v-tab-item>
    <!-- 잉~~ 부분 -->
    <v-tab-item id="tab-2">
      <v-container v-if="followings.length>0" centered class="my-0">
        <v-layout row class="my-0 py-0">
          <v-flex xs12 sm12 v-for="(items,i) in followings" :key="i">
            <FollowingList v-bind="items" :isFollowing="true" />
          </v-flex>
        </v-layout>
      </v-container>
      <v-container v-else>
        <p class="white--text subtitle-1">아직 노 팔로잉..Oops! 친구를 팔로잉해봐용</p>
      </v-container>
    </v-tab-item>
  </v-tabs>
</template>

<script>
import FollowerList from "../../components/common/FollowerList";
import FollowingList from "../../components/common/FollowingList";
import UserApi from "../../apis/UserApi";

const loginedNickname = "";
export default {
  components: {
    FollowerList,
    FollowingList
  },
  created() {
    this.getAndSetData();
  },
  methods: {
    getAndSetData() {
      this.currUserName = this.$route.params.email;
      this.loginedNickname = JSON.parse(
        sessionStorage.getItem("LoginUserInfo")
      ).nickname;
      this.getFollowerList();
      this.getFollowingList();

      if (this.loginedNickname === this.currUserName) {
        this.isMyAccount = true;
      } else {
        this.isMyAccount = false;
      }
    },
    getFollowerList() {
      console.log("팔로워를 조회할 아이디는요 ", this.currUserName);
      UserApi.requestFollowers(
        this.currUserName,
        res => {
          console.log("callback 에서 ", res);
          for (let i = 0; i < res.data.data.length; i++) {
            console.log(res.data.data[i]);
            let followerInfo = {
              nickName: res.data.data[i].nickname,
              intro: res.data.data[i].intro,
              picName: res.data.data[i].pic_name
            };

            this.followers.push(followerInfo);
          }
        },
        error => {
          console.log("에러콜백에서 ", error);
          this.$router.push({ path: "/" });
        }
      );
    },
    getFollowingList() {
      // console.log("팔로잉 조회할 아이디는요 ", this.currUserName);
      UserApi.requestFollowings(
        this.currUserName,
        res => {
          // console.log("callback 에서 ", res);
          for (let i = 0; i < res.data.data.length; i++) {
            console.log(res.data.data[i]);
            let followingInfo = {
              nickName: res.data.data[i].nickname,
              intro: res.data.data[i].intro,
              picName: res.data.data[i].pic_name
            };

            this.followings.push(followingInfo);
          }
        },
        error => {
          console.log("에러콜백에서 ", error);
          // this.$router.push({ path: "/" });
        }
      );
    }
  },
  data: () => ({
    //code
    // 1:댓글 2:좋아요 3: (나에게)팔로잉신청 4 (나의)팔로잉거절 5 팔로잉수락
    currUserName: "",
    followings: [],
    followers: [],
    isMyAccount: false
  })
};
</script>

