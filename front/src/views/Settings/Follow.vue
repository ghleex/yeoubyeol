<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <!-- 글 원문  -->
      <v-col cols="12">
        <keep-alive>
          <v-tabs centered fixed-tabs dark background-color="transparent" class="py-12">
            <v-tabs-slider color="#71d087"></v-tabs-slider>

            <v-tab href="#tab-1" @click="updateFollowerList">
              <h4>워</h4>
            </v-tab>

            <v-tab href="#tab-2" @click="updateFollowingList">
              <h4>잉</h4>
            </v-tab>

            <!-- 워 ~~~ 부분 -->
            <v-tab-item id="tab-1">
              <v-row
                v-if="followers.length>0"
                class="pt-0"
                align="start"
                justify="center"
                style="background-color:#110b22"
              >
                <v-col cols="12" v-for="(items,i) in followers" :key="i">
                  <FollowerList
                    @updateFollowerList="updateFollowerList"
                    v-bind="items"
                    :isMyAccount="isMyAccount"
                  />
                </v-col>
              </v-row>
              <v-row
                v-else
                class="pt-0"
                align="start"
                justify="center"
                style="background-color:#110b22"
              >
                >
                <p class="white--text subtitle-1">괜찮아요. 제가 친구가 되어드릴께요.</p>
              </v-row>
            </v-tab-item>
            <!-- 잉~~ 부분 -->
            <v-tab-item id="tab-2">
              <v-row
                v-if="followings.length>0"
                class="pt-0"
                align="start"
                justify="center"
                style="background-color:#110b22"
              >
                <v-col cols="12" v-for="(items,i) in followings" :key="i">
                  <FollowingList
                    @updateFollowingList="updateFollowingList"
                    v-bind="items"
                    :isMyAccount="isMyAccount"
                  />
                </v-col>
              </v-row>
              <v-row
                v-else
                class="pt-0"
                align="start"
                justify="center"
                style="background-color:#110b22"
              >
                <p class="white--text subtitle-1">혼자에 익숙해지는 중입니다.</p>
              </v-row>
            </v-tab-item>
          </v-tabs>
        </keep-alive>
      </v-col>
    </v-row>
  </v-responsive>
</template>

<script>
import FollowerList from "../../components/common/FollowerList";
import FollowingList from "../../components/common/FollowingList";
import UserApi from "../../apis/UserApi";

let loginedNickname = "";
export default {
  components: {
    FollowerList,
    FollowingList
  },
  created() {
    this.currUserName = this.$route.params.email;
    this.loginedNickname = this.$cookies.get("LoginUserInfo").nickname;
    this.checkFollowInfo(); //현재 로그인한사람의 팔로워 팔로잉정보 받아오고
    this.getAndSetData(); //조회하는 사람의 팔로워팔로잉정보 세팅
  },
  methods: {
    updateFollowerList() {
      this.checkFollowInfo();
      this.getFollowerList();
    },
    updateFollowingList() {
      this.checkFollowInfo();
      this.getFollowingList();
    },
    checkFollowInfo() {
      UserApi.requestUserProfile(
        this.loginedNickname,
        res => {
          this.LU_followers = res.data.followers;
          this.LU_followings = res.data.followings;
        },
        err => {
          this.$router.push({ path: "/404" });
        }
      );
    },
    getAndSetData() {
      this.getFollowerList();
      // this.getFollowingList();

      if (this.loginedNickname === this.currUserName) {
        this.isMyAccount = true;
      } else {
        this.isMyAccount = false;
      }
    },
    getFollowerList() {
      this.followers = [];
      UserApi.requestFollowers(
        this.currUserName,
        res => {
          for (let i = 0; i < res.data.data.length; i++) {
            let followerInfo = {
              shownNickname: res.data.data[i].nickname,
              intro: res.data.data[i].intro,
              picName: res.data.data[i].pic_name,
              //내 팔로잉 리스트와 비교해서 팔로잉인지 아닌지 알려조야해 ㅠ
              isFollowing: this.LU_followings.includes(res.data.data[i].id)
            };
            this.followers.push(followerInfo);
          }
        },
        error => {
          // this.$router.push({ path: "/" });
        }
      );
    },
    getFollowingList() {
      this.followings = [];
      UserApi.requestFollowings(
        this.currUserName,
        res => {
          for (let i = 0; i < res.data.data.length; i++) {
            let followingInfo = {
              shownNickname: res.data.data[i].nickname,
              intro: res.data.data[i].intro,
              picName: res.data.data[i].pic_name
            };

            this.followings.push(followingInfo);
          }
        },
        error => {
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
    isMyAccount: false,
    LU_followings: [],
    LU_followers: []
  })
};
</script>

