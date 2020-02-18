<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <v-col cols="12" class="py-0">
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-list dark color="#110B22">
            <v-list-item>
              <v-btn text dark small @click="backToMain">취소</v-btn>
              <v-spacer></v-spacer>
              <v-btn text dark small :disabled="!valid" @click="validate" color="#71D087">저장</v-btn>
              <br />
            </v-list-item>
            <v-list-item style="justify-content:center">
              <div v-if="url">
                <v-avatar size="150">
                  <v-img :src="url" />
                </v-avatar>
                <br />
                <v-spacer></v-spacer>
                <v-btn text class="red--text" @click="delCurrpic">X</v-btn>
              </div>
              <div v-else>
                <v-avatar size="150">
                  <v-img :src="image"></v-img>
                </v-avatar>
              </div>
            </v-list-item>
            <v-list-item style="justify-content:center">
              <form action id="imgForm">
                <input
                  type="file"
                  id="fileInput"
                  style="display:none;"
                  accept="image/*"
                  @change="onFileChanged"
                  ref="fileref"
                />

                <v-btn text onclick="document.getElementById('fileInput').click();">프로필 사진 변경</v-btn>
              </form>
            </v-list-item>
            <v-list-item>
              <v-divider></v-divider>
            </v-list-item>
            <v-list-item style="justify-content:center">
              <v-text-field
                label="닉네임"
                v-model="input.nickname"
                dark
                counter
                required
                :rules="[rules.requireValue, rules.validateKorean,rules.limitLength]"
                @keyup="isValidNickname"
              ></v-text-field>
              <!--               <v-btn text @click="isValidNickname"
              outlined>중복확인</v-btn>-->
              {{isOkay ? "✔️" : "❌" }}
            </v-list-item>
            <v-list-item>
              <v-text-field
                label="한줄 소개"
                v-model="input.intro"
                dark
                :rules="rules.introRules"
                counter
              ></v-text-field>
            </v-list-item>
            <v-list-item>
              <v-btn block outlined @click="changePassword">비밀번호 변경</v-btn>
            </v-list-item>
          </v-list>
        </v-form>
      </v-col>
    </v-row>
  </v-responsive>
</template>

<script>
import UserApi from "@/apis/UserApi";
import dotenv from "dotenv";
import axios from "axios";

dotenv.config();
export default {
  created() {
    let userInfo = this.$cookies.get("LoginUserInfo");
    this.loginedNickname = userInfo.nickname;
    this.getUserInformation();
  },
  data() {
    return {
      valid: false,
      loginedNickname: "",
      user: {
        id: "",
        intro: "",
        nickname: "",
        username: "",
        picname: ""
      },
      input: {
        intro: "",
        nickname: ""
      },
      image: "",
      url: "",
      selectedFile: "",
      isOkay: true,

      rules: {
        requireValue: value =>
          (!!value && value.trim().length > 0) || "입력해주세요!",
        limitLength: value => value.trim().length < 20 || "너무 길어요",
        introRules: [
          value => !!value || "소개를 입력해주세요!",
          value => value.trim().length <= 50 || "너무 길어요"
        ],
        validateKorean: v =>
          !/[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/.test(v) || "한글을 제외하고 입력해주세요."
      }
    };
  },
  methods: {
    changePassword() {
      this.$router.push({ name: "비밀번호변경"});
    },
    backToMain() {
      this.$router.push({ name: "메인피드" });
    },
    delCurrpic() {
      this.url = "";
      this.selectedFile = "";
      this.$refs.fileref.value = "";
    },
    onFileChanged(event) {
      this.selectedFile = event.target.files[0];
      this.url = URL.createObjectURL(this.selectedFile);
    },
    validate() {
      if (this.$refs.form.validate()) {
        //저장하는 메소드 들어가야함
        if (this.isOkay) {
          this.editUsersProfileToServer();
        } else {
          alert("닉네임에 ✔️를 만들어주세요 !");
        }
      }
    },
    editUsersProfileToServer() {
      let data = new FormData();
      data.append("username", this.user.id);
      data.append("pic_name", this.selectedFile);
      data.append("nickname", this.input.nickname);
      data.append("intro", this.input.intro);
      UserApi.editUsersProfile(
        data,
        res => {
          alert("정보 변경이 완료되었어요 !");
          console.log(res);
          const LoginUserInfo = {
            username: data.email,
            nickname: res.data.nickname,
            id: res.data.id,
            pic_name: res.data.pic_name
          };
          let userData = JSON.stringify(LoginUserInfo);
          this.$cookies.set("LoginUserInfo", userData, 0);

          // console.log(res);
          this.$router.push({
            name: "프로필",
            params: { email: this.input.nickname }
          });
        },
        error => {
          console.log(error);
        }
      );
    },
    isValidNickname() {
      if (this.input.nickname.trim() === this.user.nickname.trim()) {
        this.isOkay = true;
        return;
      }
      let temp = this.input.nickname.replace(/(\s*)/g, "");
      this.input.nickname = temp;
      let nickname = new FormData();
      nickname.append("nickname", temp);
      UserApi.checkNicknameAvaliable(
        nickname,
        res => {
          this.isOkay = true;
        },
        error => {
          this.isOkay = false;
        }
      );
    },
    getUserInformation() {
      UserApi.requestUserProfile(
        this.loginedNickname,
        res => {
          let sentData = JSON.stringify(res.data);
          console.log("프로필1111 : " + JSON.stringify(res.data));
          this.user.id = res.data.id;
          this.user.intro = res.data.intro;
          this.user.nickname = res.data.nickname;
          this.user.username = res.data.username;
          this.user.picname = `${process.env.VUE_APP_IP}${res.data.pic_name}`;

          //temp data
          this.input.intro = this.user.intro;
          this.input.nickname = this.user.nickname;

          this.image = this.user.picname;
        },
        err => {
          this.$router.push({ path: "/error" });
        }
      );
    }
  }
};
</script>

<style>
</style>