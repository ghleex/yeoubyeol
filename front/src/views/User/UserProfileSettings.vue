<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <!-- 글 원문  -->
      <v-col class="d-flex justify-end mr-3">
        <v-btn text dark small>
          취소
        </v-btn>
        <v-btn text dark small color="#71D087">
          저장
        </v-btn>
      </v-col>
      <v-col cols="12" class="d-flex justify-center">
        <!-- 프로필 사진 -->
        <v-btn absolute text dark top>프로필 사진 변경</v-btn>
        <v-avatar size="150">
          <v-img :src="image"></v-img>
        </v-avatar>
      </v-col>
      <v-col cols="12" class="d-flex justify-center" style="max-width: 400px; margin: auto;">
        <v-text-field 
          label="닉네임" 
          v-model="user.nickname" 
          dark
          :rules="[rules.requireValue, rules.validateKorean]"></v-text-field>
        <v-btn text @click="checkNickname" dark>중복확인</v-btn>
      </v-col>
      <v-col cols="12" class="d-flex justify-center" style="max-width: 400px; margin: auto;">
        <v-text-field 
          label="한줄 소개" 
          v-model="user.intro" 
          dark
          :rules="[]"></v-text-field>
      </v-col>
    </v-row>
  </v-responsive>
</template>

<script>
import UserApi from '@/apis/UserApi'
import dotenv from 'dotenv';
import axios from 'axios';

dotenv.config();
export default {
  created() {
    let userInfo = this.$cookies.get('LoginUserInfo');
    this.loginedNickname = userInfo.nickname;
    this.getUserInformation();
  },
  data() {
    return {
      loginedNickname: '',
      user: {
        id: '',
        intro: '',
        nickname: '',
        username: '',
        picname: '',
      },
      image: '',
      selectedFile: '',
      isChanged: false,
      isTest: false,

      rules: {
        requireValue: value => !!value || '입력해주세요!',
        validateNickname: value => this.checkNickname() || '중복된 이름입니다.',
        validateKorean: v => !/[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/.test(v) || '한글을 제외하고 입력해주세요.',
      }
    }
  },
  methods: {
    checkNickname() {
      let nickname = new FormData();
      nickname.append('nickname', this.user.nickname)

      axios.post(`http://${process.env.VUE_APP_IP}/accounts/checknickname/`, nickname)
        .then(response => {
          console.log('굳')
          console.log(response)
          this.isTest = true
        })
        .catch(error => {
          console.log(error)
          if (error.status === 400) {
            this.isTest = '중복된 이름입니다.'
          } else {
            this.isTest = false
          }
        })
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
          this.user.picname = require("@/assets/images/profile/" + res.data.pic_name + ".png");
          this.image = this.user.picname;
        },
        err => {
          this.$router.push({ path: "/404" });
        }
      );
    },
  }
}
</script>

<style>

</style>