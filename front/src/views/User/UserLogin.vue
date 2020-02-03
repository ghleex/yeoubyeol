
<template>
  <v-card dark color="#110b22">
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-container fluid class="py-3">
        <v-row no-gutters justify="space-between" align="center">
          <v-col cols="12" class="pt-2">
            <h1>
              새벽이 되면
              <br />다르게 보일거에요.
            </h1>
            <img src="../../assets/images/여우별(밤).png" alt width="100px" />
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
              hint="영문,숫자 포함 8자리 이상, 15자리 이하입니다."
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
            >로그인</v-btn>
            <v-spacer></v-spacer>
          </v-col>

          <v-col cols="12">
            <router-link v-bind:to="{name:'비밀번호 변경'}">
            <v-btn  text min-width="100" class="px-0 my-3">비밀번호 찾기</v-btn>
              </router-link>
              <v-btn  text disabled></v-btn>
             <router-link v-bind:to="{name:'인증메일 발송'}" style="color: #00edd6">
            <v-btn text min-width="100" class="px-0 my-3">함께 하기</v-btn>
               </router-link>
          </v-col>

          <v-col class="pt-20" cols="12">
            <v-btn text class="g-signin2" data-onsuccess="onSignIn">
              <v-icon>mdi-google</v-icon>구글로 로그인
            </v-btn>
            <a href="#" onclick="signOut();" style="border: 1px solid #EEEEEE;">Sign out</a>
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

import "../../assets/css/style.scss";
import "../../assets/css/user.scss";
import PV from "password-validator";
import axios from 'axios'
import * as EmailValidator from "email-validator";
import UserApi from "../../apis/UserApi";

let tokenFromLogin='';
export default {
  created() {
    if (sessionStorage.getItem("AUTH_token")) {
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
              alert("로그인되었습니다.");
              
              //요청이 끝나면 버튼 활성화
              let data={'email':email};
              console.log('프로필조회 : '+data.email);
              axios.post(`http://192.168.31.80:8000/accounts/`, data).then((response=>{
                console.log('로그인 후 가져온 다라 '+response.data[0].nickname);
                  sessionStorage.setItem("AUTH_token", this.tokenFromLogin);
                  sessionStorage.setItem('LoginUserNickname',response.data[0].nickname);
                  router.push({ name: "홈" });
              }),error=>{
                console.log("로그인 후 프로필 가져오기 문제");
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
      v => /.+@.+\..+/.test(v) || "이메일 형식이 아닙니다."
    ],
    password: "",
    passwordRules: [
      v =>
        !!v ||
        "비밀번호는 영문,숫자,특수문자포함 8자리 이상, 15자리 이하입니다",
      v =>
        (v.length <= 15 && v.length >= 8) ||
        "비밀번호는 영문,숫자,특수문자포함 8자리 이상, 15자리 이하입니다"
    ],

    alert: false,
    isSubmit: false
  })
};
</script>


