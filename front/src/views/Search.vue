<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <v-col cols="12">
     <v-list dark color="#110B22">
          <v-list-item>
        <v-text-field v-model="keyword" name="search" label="키워드를 입력하세요" @keyup.enter="search"></v-text-field>

        <v-btn text small class="px-0">
          <v-icon @click="search()">mdi-magnify</v-icon>
        </v-btn>
          </v-list-item>
     </v-list>

    <!-- 탭  메뉴 -->
    <div v-if="isSearched" class="py-2">
      <v-tabs centered fixed-tabs dark background-color="transparent" class="py-0">
        <v-tabs-slider color="#71d087"></v-tabs-slider>

        <v-tab href="#tab-1">키워드</v-tab>

        <v-tab href="#tab-2">유저</v-tab>

        <!--  결과 - 키워드탭 -->
        <v-tab-item id="tab-1">
           <v-row   v-if="SearchKeywordResult.length>0" class="pt-0" align="start" justify="center" style="background-color:#110b22">
              <v-col cols="12" xs12 sm12 v-for="(items,i) in SearchKeywordResult" :key="i">
                <SearchKeyword v-bind="items" />
              </v-col>
            </v-row>
          <v-row v-else  class="pt-0" align="start" justify="center" style="background-color:#110b22">
            <p class="white--text subtitle-1">검색 결과가 없어여</p>
          </v-row>
        </v-tab-item>
        <!-- 결과 - 유저-->
        <v-tab-item id="tab-2">
          <v-row   v-if="SearchUserResult.length>0" class="pt-0" align="start" justify="center" style="background-color:#110b22">
              <v-col cols="12" xs12 sm12 v-for="(items,i) in SearchUserResult" :key="i" @click="gotoUserPfPage(items.nickname)">
              <SearchUser v-bind="items" />
              </v-col>
            </v-row >
          <v-row v-else  class="pt-0" align="start" justify="center" style="background-color:#110b22">
            <p class="white--text title">노 result ... </p>
          </v-row>
        </v-tab-item>
      </v-tabs>
    </div>

    <!-- 최근검색 구역 -->
    <div class="py-1" v-else>
      <div v-if="Object.keys(searchedHistory).length>0">
        <v-card
          dark
          color="#110b22"
          style="border: 1px solid #110b22"
          v-for="kw in Object.keys(searchedHistory)"
          :key="kw"
          class="py-0 my-0"
        >
          <v-card-actions class="px-1 py-1">
            <v-list-item class="grow px-2 py-0">
              <v-list-item-content>
                <h3>{{searchedHistory[kw]}}</h3>
              </v-list-item-content>
            </v-list-item>
          </v-card-actions>
        </v-card>
        <v-btn block text class="red--text" @click="delSearchedKeyword">기록 전체 삭제</v-btn>
      </div>
      <div v-else class="py-4">
        <h2 class="white--text">검색기록이 없어요.</h2>
      </div>
    </div>
 </v-col>
    </v-row>
  </v-responsive>
</template>

<script>
import SearchUser from "../components/common/SearchUser";
import SearchKeyword from "../components/common/SearchKeyword";

import SearchApi from "../apis/SearchApi";
export default {
  components: {
    SearchUser,
    SearchKeyword
  },

  data: () => ({
    keyword: "",
    isSearched: false,
    searchedHistory: {},
    //code
    // 1:댓글 2:좋아요 3: (나에게)팔로잉신청 4 (나의)팔로잉거절 5 팔로잉수락
    SearchKeywordResult: [
      {
        keyword: "우리팀 ~~!"
      },
      {
        keyword: "예쁘게"
      },
      {
        keyword: "봐주세요"
      }
    ],
    SearchUserResult: []
  }),
  methods: {
    search() {
      // console.log("검색쿠 :" + this.keyword);
      if (this.keyword.trim() !== "") {
        this.isSearched = true;

        let { keyword } = this;
        let data = { keyword };

        try {
          //여기에 검색쿠 가자
          SearchApi.SearchUser(
            data,
            res => {
              if (res.data.length === 0) {
                this.SearchUserResult = [];
              } else {
                this.SearchUserResult = [];
                for (
                  let i = 0;
                  i < res.data.length;
                  i++
                ) {
                  // console.log(res.data.nicknames_serializer_data[i].nickname);
                  this.SearchUserResult.push({
                    nickname: res.data[i].nickname,
                    pic_name:   require("@/assets/images/profile/" +
                res.data[i].pic_name +
                ".png"),
                    intro : res.data[i].intro,
                  });
                }
              }
            },
            error => {
              console.log("에러");
            }
          );
          let searchHistory = JSON.parse(localStorage.getItem("searchHistory"));
          searchHistory.push(this.keyword);
          localStorage.setItem("searchHistory", JSON.stringify(searchHistory));
        } catch {
          let searchHistory = new Array(this.keyword);
          localStorage.setItem("searchHistory", JSON.stringify(searchHistory));
        }
      }else{
        alert("검색어를 입력해주세요 .");
      }
    },
    delSearchedKeyword() {
      localStorage.clear();
      this.searchedHistory = {};
    },
    gotoUserPfPage(id) {
      //페이지 이동을 어떠카지...
      this.$router.push({ name: "프로필", params: { email: id } });
    }
  },
  watch: {
    keyword: function(v) {
      if (this.keyword === "") {
        this.isSearched = false;
        this.searchedHistory = JSON.parse(
          localStorage.getItem("searchHistory")
        );
      }
    }
  },
  created() {
    // this.searchedHistory = this.$store.getters.getsearchHistory;
    console.log(this.searchedHistory);
  }
};
</script>

