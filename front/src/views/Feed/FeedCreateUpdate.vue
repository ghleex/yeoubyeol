<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <!-- <v-col cols="12" dark style="backgroundImage:url('../../assets/images/moon_home.jpg)"> -->
      <v-col cols="12" dark :style="bgByWeather">
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-row class="py-0 ma-2">
            <v-col cols="4" class="px-0">
              <v-btn dark text>취소</v-btn>
            </v-col>
            <v-col cols="4" dark class="timer px-0 white--text text-center d-flex justify-center">
              <v-img :src="weather_url" max-width="40" max-height="40"></v-img>
              {{ lastTime }}
            </v-col>
            <v-col cols="4" class="pl-0 pr-1 d-flex justify-end">
              <v-btn
                class="mb-2"
                color="#71d087"
                style="color:#110b22;"
                @click="validate"
                :disabled="!valid"
              >{{postId>0 ? "수정": "작성"}}</v-btn>
            </v-col>
            <v-col cols="12" class="pa-0">
              <div id="preview">
                <img v-if="url" :src="url" style="padding-bottom:5px" />
                <br />
              </div>
              <v-file-input
                dark
                id="fileInput"
                accept="image/*"
                prepend-icon="mdi-camera"
                outlined
                dense
                required
                :clearable="false"
                label="Image"
                @change="onFileChanged"
              ></v-file-input>
            </v-col>
            <v-col cols="12" class="pa-1">
              <v-textarea
                dark
                :rules="contentRules"
                required
                outlined
                v-model="inputPostContent"
                :autofocus="true"
                :auto-grow="true"
                clearable
                rows="8"
              >{{inputPostContent}}</v-textarea>
            </v-col>
            <v-col cols="12" class="pa-1">
              <v-btn
                @click="requestHashTags"
                text
                block
                style="color:#71d087;"
                class="ma-1"
              >해시태그 추천받기</v-btn>
              <v-progress-linear :active="loading" :indeterminate="loading" absolute color="green"></v-progress-linear>

              <!-- 여기부터 시작야이             -->
            </v-col>

            <v-col cols="12" class="pa-1">
              <v-combobox
                dark
                v-model="model"
                :filter="filter"
                :hide-no-data="!search"
                :items="items"
                :search-input.sync="search"
                hide-selected
                label="Search for an option"
                multiple
                small-chips
                solo
              >
                <template v-slot:no-data>
                  <v-list-item>
                    <span class="subheading">추가하기</span>
                    <v-chip color="darkgrey" label small>{{ search }}</v-chip>
                  </v-list-item>
                </template>
                <template v-slot:selection="{ attrs, item, parent, selected }">
                  <v-chip
                    v-if="item === Object(item)"
                    v-bind="attrs"
                    color="darkgrey"
                    :input-value="selected"
                    label
                    small
                  >
                    <span class="pr-2">{{ item.text }}</span>
                    <v-icon small @click="parent.selectItem(item)">mdi-close</v-icon>
                  </v-chip>
                </template>
                <template v-slot:item="{ index, item }">
                  <v-text-field
                    v-if="editing === item"
                    v-model="editing.text"
                    autofocus
                    flat
                    background-color="transparent"
                    hide-details
                    solo
                    @keyup.enter="edit(index, item)"
                  ></v-text-field>
                  <v-chip v-else color="darkgrey" dark label small>{{ item.text }}</v-chip>
                  <v-spacer></v-spacer>
                  <v-list-item-action @click.stop>
                    <v-btn icon @click.stop.prevent="edit(index, item)">
                      <v-icon>{{ editing !== item ? 'mdi-pencil' : 'mdi-check' }}</v-icon>
                    </v-btn>
                  </v-list-item-action>
                </template>
              </v-combobox>
            </v-col>
          </v-row>
        </v-form>
      </v-col>
    </v-row>
  </v-responsive>
</template>

<script>
import FeedApi from "@/apis/FeedApi";
import dotenv from "dotenv";

dotenv.config();

const API_KEY = "927a607b0b357ff6efcbabbd85795740";
const WEATHER_API = "https://api.openweathermap.org/data/2.5/weather?";

export default {
  created() {
    //time check
    let date = new Date();
    let currHour = date.getHours();
    //냠
    if (!(currHour >= 9 && currHour < 17)) {
      alert(
        "지금은 작성 가능한 시간이 아니에요 ..(작성가능한 시간은 현재 오전 9시 ~ 오후 5시 입니다.)"
      );
      this.$router.push({ name: "메인피드" });
    }

    let userInfo = this.$cookies.get("LoginUserInfo");
    if (this.$route.params.postId > 0) {
      this.postId = this.$route.params.postId;
    }
    if (this.postId > 0) {
      //게시글 수정인 경우
      this.getArticleByIdBindingData(this.postId);
    }
    this.loadWeather();
    this.loginedNickname = userInfo.nickname;
    this.timeCalc = setInterval(() => {
      this.getTime();
    }, 1000);
  },

  beforeRouteLeave(to, from, next) {
    clearInterval(this.timeCalc);
    return next();
  },

  computed: {
    bgByWeather: function() {
      let min = 1;
      let calc_name = "d1.gif";
      if (this.weather_id >= 200 && this.weather_id < 600) {
        //비
        let max = 4;
        let name = Math.floor(Math.random() * max) + min;
        calc_name = `r${name}.gif`;
      } else if (this.weather_id >= 600 && this.weather_id < 700) {
        //눈
        let max = 2;
        let name = Math.floor(Math.random() * max) + min;
        calc_name = `s${name}.gif`;
      } else if (this.weather_id >= 700 && this.weather_id < 900) {
        //맑음이나 흐림 안개
        let max = 5;
        let name = Math.floor(Math.random() * max) + min;
        calc_name = `m${name}.gif`;
      }
      return {
        "background-image":
          "url(" + require("@/assets/images/bg/" + calc_name) + ")",
        "background-position": "center",
        "background-repeat": "no-repeat",
        "background-size": "cover"
      };
    }
  },
  methods: {
    editPostDone() {
      let date = new Date();
      let currHour = date.getHours();
      if (currHour >= 9 && currHour < 17) {
        let tagLists = [];
        for (let i = 0; i < this.model.length; i++) {
          tagLists.push(this.model[i].text);
        }
        let form = {
          id: this.postId,
          article: this.inputPostContent,
          image: this.selectedFile,
          hashtags: tagLists
        };
        FeedApi.editPost(
          form,
          res => {
            alert("수정 완료 ! ");
            this.$router.push({ name: "댓글", params: { id: this.postId } });
          },
          error => {
            alert("수정에 에러가 발생했어요 ");
          }
        );
      } else {
        alert("지금은 글 수정이 가능한 시간이 아니에요 ..");
      }
    },
    getArticleByIdBindingData(id) {
      FeedApi.getArticleById(
        id,
        res => {
          //성공시
          //article
          this.url = `${process.env.VUE_APP_IP}${res.data.article.image}`;
          this.inputPostContent = res.data.article.article;
          this.model = [];
          for (let i = 0; i < res.data.hashtags.length; i++) {
            this.model.push({ text: res.data.hashtags[i] });
          }
          // res.data.hashtags,
        },
        error => {
          alert("게시글을 불러오는데 실패했어요 ..");
          this.$router.push({ name: "댓글", params: { id: this.postId } });
        }
      );
    },
    requestHashTags() {
      let form = new FormData();
      form.append("article", this.inputPostContent);
      this.loading = true;
      FeedApi.requestHashTags(
        form,
        res => {
          this.items = [];
          this.items.push({
            header: "아래 중 하나를 입력하거나, 새로 입력해보세요!"
          });
          let temp = [];
          for (let i = 0; i < this.model.length; i++) {
            temp.push(this.model[i].text);
          }
          for (let i = 0; i < res.data.length; i++) {
            if (!temp.includes(res.data[i])) {
              this.model.push({
                text: res.data[i]
              });
              this.items.push({ text: res.data[i] });
            }
          }
          this.loading = false;
        },
        error => {
          this.loading = false;
        }
      );
    },
    edit(index, item) {
      if (!this.editing) {
        this.editing = item;
        this.index = index;
      } else {
        this.editing = null;
        this.index = -1;
      }
    },
    filter(item, queryText, itemText) {
      if (item.header) return false;

      const hasValue = val => (val != null ? val : "");

      const text = hasValue(itemText);
      const query = hasValue(queryText);

      return (
        text
          .toString()
          .toLowerCase()
          .indexOf(query.toString().toLowerCase()) > -1
      );
    },
    onFileChanged(event) {
      this.selectedFile = event;
      this.url = URL.createObjectURL(this.selectedFile);
    },
    validate() {
      if (this.$refs.form.validate()) {
        // this.snackbar = true;
        if (this.postId < 0) {
          this.newPost();
        } else {
          this.editPostDone();
        }
      }
    },
    newPost() {
      if (this.selectedFile == "") {
        alert("사진을 등록해 주세요!");
        return;
      }
      let date = new Date();
      let currHour = date.getHours();
      //냠
      if (currHour >= 9 && currHour < 17) {
        let form = new FormData();
        let tagLists = [];
        for (let i = 0; i < this.model.length; i++) {
          tagLists.push(this.model[i].text);
        }

        let token = this.$cookies.get("auth_cookie");
        form.append("token", token);
        form.append("nickname", this.loginedNickname);
        form.append("article", this.inputPostContent);
        form.append("image", this.selectedFile);
        form.append("hashtags", tagLists);
        FeedApi.newPost(
          form,
          res => {
            alert("글이 성공적으로 게시되었습니다.");
            this.$router.push({ name: "댓글", params: { id: res.data.id } });
          },
          error => {}
        );
      } else {
        alert("지금은 작성 가능한 시간이 아니에요.");
      }
    },
    // weatherapi -----------------------
    getWeather(coords) {
      fetch(
        `${WEATHER_API}lat=${coords.lat}&lon=${coords.lng}&appid=${API_KEY}&units=metric`
      )
        .then(response => response.json())
        .then(json => {
          const name = json.name;
          const temperature = json.main.temp;
          // this.data = json;
          this.weather_id = json.weather[0].id;
          this.weather_icon = json.weather[0].icon;
          this.weather_url = `http://openweathermap.org/img/w/${this.weather_icon}.png`;
          this.weather_detail = `${Math.floor(temperature)}° @ ${name}`;
        });
    },

    handleGeoSuccess(position) {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;
      const coords = {
        lat,
        lng
      };
      localStorage.setItem("coords", JSON.stringify(coords));
      this.getWeather(coords);
    },

    handleGeoFailure() {
      alert("새로고침 해주세요!");
    },

    loadWeather() {
      const currentCoords = localStorage.getItem("coords");
      if (currentCoords !== null) {
        const parsedCoords = JSON.parse(currentCoords);
        this.getWeather(parsedCoords);
        return;
      } else {
        navigator.geolocation.getCurrentPosition(
          this.handleGeoSuccess,
          this.handleGeoFailure
        );
      }
    },
    getTime() {
      const now = new Date();
      const hours = now.getHours();
      const minutes = now.getMinutes();
      const seconds = now.getSeconds();

      const baseTime = new Date();
      let newDate = baseTime.getDate() + 1;
      if (hours >= 17) {
        baseTime.setDate(newDate);
      }
      baseTime.setHours(17);
      baseTime.setMinutes(0);
      baseTime.setSeconds(0);

      const diffTime = (baseTime - now) / 1000;
      let lastHours = diffTime / 3600;
      if (0 <= lastHours && lastHours < 10) {
        lastHours = `0${Math.floor(lastHours)}`;
      } else if (lastHours < 0 || isNaN(lastHours)) {
        lastHours = "00";
      } else {
        lastHours = Math.floor(lastHours);
      }

      let lastMinutes = (diffTime % 3600) / 60;
      if (0 <= lastMinutes && lastMinutes < 10) {
        lastMinutes = `0${Math.floor(lastMinutes)}`;
      } else if (lastMinutes < 0 || isNaN(lastMinutes)) {
        lastMinutes = "00";
      } else {
        lastMinutes = Math.floor(lastMinutes);
      }

      let lastSeconds = (diffTime % 3600) % 60;
      if (0 <= lastSeconds && lastSeconds < 10) {
        lastSeconds = `0${Math.floor(lastSeconds)}`;
      } else if (lastSeconds < 0 || isNaN(lastSeconds)) {
        lastSeconds = "00";
      } else {
        lastSeconds = Math.floor(lastSeconds);
      }

      const Time = `${lastHours}:${lastMinutes}:${lastSeconds}`;
      this.lastTime = Time;

      if (this.lastTime === "24:00:00") {
        alert("이제 잠에서 깰 시간이에요.");
        var router = this.$router;
        router.push({ name: "홈" });
      }
    }
  },
  data: () => {
    return {
      timeCalc: "",
      loading: false,
      postId: -1,
      weather_id: null,
      weather_icon: "",
      weather_detail: "",
      weather_url: "",
      activator: null,
      attach: null,
      editing: null,
      url: null,
      index: -1,
      items: [{ header: "아래 중 하나를 입력하거나, 새로 입력해보세요!" }],
      nonce: 1,
      menu: false,
      model: [
        {
          text: "감성"
        }
      ],
      x: 0,
      search: null,
      y: 0,

      loginedNickname: "",
      selectedFile: "",
      inputPostContent: "",
      hash_check: false,
      valid: false,
      contentRules: [v => !!v || "내용을 입력해주세요.."],
      lastTime: ""
    };
  },
  watch: {
    model(val, prev) {
      if (val.length === prev.length) return;

      this.model = val.map(v => {
        if (typeof v === "string") {
          v = {
            text: v
          };

          this.items.push(v);

          this.nonce++;
        }

        return v;
      });
    }
  }
};
</script>
<style scoped>
#preview {
  display: flex;
  justify-content: center;
  align-items: center;
}

#preview img {
  max-width: 50%;
  max-height: 100px;
}

.timer {
  font-family: "ZCOOL QingKe HuangYou", cursive;
  font-size: 24px;
}
</style>