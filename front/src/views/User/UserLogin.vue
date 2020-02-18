
<template>
  <v-card dark color="#110b22">
    <v-form ref="form" v-model="valid" lazy-validation @submit.prevent="validate">
      <v-container fluid class="py-3">
        <v-row no-gutters justify="space-between" align="center">
          <v-col cols="12" class="pt-2">
            <h1>
              새벽이 되면
              <br />다르게 보일거에요.
            </h1>
            <!-- <img src="../../assets/images/여우별(밤).png" alt width="100px" /> -->
            <br>
          </v-col>
          <v-col cols="12">
            <v-text-field
              outlined
              v-model="email"
              :rules="emailRules"
              label="이메일"
              hint="이메일입력 필수"
              required
            ></v-text-field>

            <v-text-field
              outlined
              v-model="password"
              :rules="passwordRules"
              type="password"
              label="비밀번호"
              hint="영문,숫자 포함 8자리 이상, 20자리 이하입니다."
              required
            ></v-text-field>
          </v-col>

          <!-- <v-checkbox
      v-model="checkbox"
      :rules="[v => !!v || '동의하지 않으면 가입할 수 없습니다.']"
      label="Do you agree?"
      required
          ></v-checkbox>-->
          <v-col cols="12">
            <v-btn
              min-height="50"
              block
              :disabled="!valid"
              color="#71d087"
              style="color:#110b22"
              @click="validate"
              @keyup.enter="validate"
            >로그인</v-btn>
          </v-col>
          
          <v-col cols="12" class="mt-5">
            <GoogleLogin 
              :params="params" 
              :onSuccess="onSuccess" 
              :onFailure="onFailure"
              style="width: 100%; height: 50px; border-radius: 5px; background-color: white; color: #110b22; font-family: 'Roboto'; display: flex; justify-content: center; align-content: center;"
            >
              <v-icon color="#110b22">mdi-google</v-icon> <span><strong>oogle</strong>로 로그인</span>
            </GoogleLogin>
            <!-- <div class="g-signin2" data-onsuccess="onSignIn" style="display: flex; flex-direction: column;"></div>
            <a href="#" onclick="signOut();">Sign out</a> -->
          </v-col>

          <v-col cols="12" class="d-flex justify-space-around px-12">
            <router-link v-bind:to="{name:'비밀번호 변경'}">
            <v-btn  text min-width="100" class="px-0 my-3">비밀번호 찾기</v-btn>
              </router-link>
              <v-btn  text disabled></v-btn>
             <router-link v-bind:to="{name:'인증메일 발송'}" style="color: #00edd6">
            <v-btn text min-width="100" class="px-0 my-3">함께 하기</v-btn>
               </router-link>
          </v-col>

        </v-row>
        <v-alert
          v-model="alert"
          dismissible
          type="warning"
          color="#F15050"
          class="py-2"
        >이메일과 비밀번호를 확인해주세요...</v-alert>
      </v-container>
    </v-form>
  </v-card>
</template>

<script>
import GoogleLogin from 'vue-google-login';
import "../../assets/css/style.scss";
import "../../assets/css/user.scss";
import PV from "password-validator";
import axios from 'axios'
import * as EmailValidator from "email-validator";
import UserApi from "../../apis/UserApi";

import dotenv from 'dotenv';

dotenv.config();

let tokenFromLogin='';
export default {
  created() {
    if (sessionStorage.getItem("refresh_token")) {
      alert("이미 로그인된 상태입니다.");
      var router = this.$router;
      router.push({ name: "홈" });
    }

    if (this.$store.error) {
      this.email = this.$store.error;
      this.$store.error = null;
    }
  },
  methods: {
    onSuccess(googleUser) {
      var profile = googleUser.getBasicProfile();
      console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
      console.log('Name: ' + profile.getName());
      console.log('Image URL: ' + profile.getImageUrl());
      console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.

      var id_token = googleUser.getAuthResponse().id_token;
      console.log('ID_TOKEN: ' + id_token)

      var form = new FormData();
      form.append('id_token', id_token)
      axios.defaults.xsrfCookieName = 'csrftoken'
      axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
      axios.post(`${process.env.VUE_APP_IP}/accounts/google/`, form)
        .then(response => {
          console.log(response)
          const LoginUserInfo={
            username: response.data.username,
            nickname : response.data.nickname,
            id : response.data.id,
            pic_name:response.data.pic_name
          }
          let userData = JSON.stringify(LoginUserInfo)

          this.$cookies.set('LoginUserInfo', userData, 0)
          this.$cookies.set('auth_cookie', id_token, 0)
          this.$cookies.set('username', response.username, 0)

          var userInfo = new FormData();
          userInfo.append('username', response.data.username)
          userInfo.append('token_1', id_token)
          
          var router = this.$router
          axios.post(`${process.env.VUE_APP_IP}/accounts/check/`, userInfo)
            .then(response => {
              let refresh_token = response.data.token_2
              sessionStorage.setItem('refresh_token', refresh_token)
              alert('3단계')
              router.push({ name: '메인피드'})
              alert('4단계')
            })
            .catch(error => {
              alert('로그인 실패')
              router.push({ name: "홈" });
            })
        })
        .catch(error => {
        console.log(error)
        })
    },
    onFailure(error) {
      console.log(error)
    },
    validate() {
      if (this.$refs.form.validate()) {
        // this.snackbar = true;
        this.isSubmit = true;
        this.login();
      }
    },
    login() {
      if (this.isSubmit) {
        let { email, password } = this;
        let data = {
          email,
          password
        };

        //요청 후에는 버튼 비활성화
        this.isSubmit = false;

        UserApi.requestLogin(
          data,
          res => {
            //통신을 통해 전달받은 값 콘솔에 출력
            // console.log("Success");
            // console.log(res);
            var router = this.$router;
            this.tokenFromLogin = res.data.token;
            if (res.status === 200) {
              alert("1단계");
              
              //요청이 끝나면 버튼 활성화
              let data={'email':email};
              console.log('프로필조회 : '+data.email);
              axios.post(`${process.env.VUE_APP_IP}/accounts/`, data).then((response=>{
                console.log('로그인 후 가져온 다라 '+response.data[0].nickname);
                console.log("login -> ",response.data[0]);
                  const LoginUserInfo={
                    username: data.email,
                    nickname : response.data[0].nickname,
                    id : response.data[0].id,
                    pic_name:response.data[0].pic_name
                  }
                  let userData = JSON.stringify(LoginUserInfo)

                  this.$cookies.set('LoginUserInfo', userData, 0)
                  this.$cookies.set('auth_cookie', this.tokenFromLogin, 0)
                  this.$cookies.set('username', data.email, 0)
                  
                  var userInfo = new FormData();
                  userInfo.append('username', data.email)
                  userInfo.append('token_1', this.tokenFromLogin)
                  console.log(data.email)
                  console.log(this.tokenFromLogin)

                  axios.post(`${process.env.VUE_APP_IP}/accounts/check/`, userInfo)
                    .then(response => {
                      console.log('---------------------------------')
                      let refresh_token = response.data.token_2
                      console.log(refresh_token)
                      sessionStorage.setItem('refresh_token', refresh_token)
                      alert('3단계')
                      router.push({ name: '메인피드'})
                      alert('4단계')
                    })
                    .catch(error => {
                      console.log('++++++++++++++++++++++++++++++++++')
                      alert('로그인 실패')
                      router.push({ name: "홈" });
                    })
              }),error=>{
                console.log("로그인 후 프로필 가져오기 문제");
                alert('뭔가 문제가 있어')
              })
    
            } else {
              // console.log("Fail");
              this.password = "";
              this.alert = true;

              //요청이 끝나면 버튼 활성화
              this.isSubmit = true;
            }
          },
          error => {
            this.password = "";
              this.alert = true;
          }
        );
      }
    }
  },
  data: () => ({
    valid: false,
    loginFail: false,
    email: "",
    emailRules: [
      v => !!v || "이메일 형식이 아닙니다.",
      v => !/\s/.test(v) || '공백없이 입력해주세요.',
      v => /.+@.+\..+/.test(v) || "이메일 형식이 아닙니다.",
    ],
    password: "",
    passwordRules: [
      v =>
        !!v ||
        "비밀번호는 영문,숫자,특수문자포함 8자리 이상, 20자리 이하입니다",
      v => !/\s/.test(v) || '공백없이 입력해주세요.',
      v =>
        /^.*(?=^.{8,20}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[`~!@#$%^&+=;',.?]).*$/.test(v) || "비밀번호는 영문,숫자,특수문자포함 8자리 이상, 20자리 이하입니다",
    ],

    alert: false,
    isSubmit: false,

    params: {
      client_id: "832271626552-bpmo24c8a7e1s2lfhs1jfl0ena583jt1.apps.googleusercontent.com"
    },
    // only needed if you want to render the button with the google ui
    renderParams: {
      longtitle: true
    }
  }),
  components: {
    GoogleLogin
  }
};
</script>