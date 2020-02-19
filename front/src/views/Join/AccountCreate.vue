
<template>
  <v-card dark color="#110b22">
   
      <v-container fluid class="py-3">
        <v-row no-gutters justify="space-between" align="center">
          <v-col cols="12">
            <h1 class="display-1 font-weight-black my-8">
              당신을
              <br />기다리고
              <br />있습니다.
              <br />
            </h1>
          </v-col>
          <v-col cols="12">
            <v-list dark color="#110b22">
              <v-list-item style="justify-content:center">
                <v-text-field
                  v-model="form.nickName"
                  :rules="[rules.requiredNickname, rules.validateKorean,rules.limitLength, rules.hasSpace]"
                  name="nickname"
                  label="닉네임"
                  id="nickname"
                  hint="영문과 숫자만 사용하여 입력해주세요."
                  outlined
                  dense
                  @keyup="isValidNickname"
                ></v-text-field>
                {{isOkay ? "✔️" : "❌" }}
              </v-list-item>
               <v-form ref="form" v-model="valid" lazy-validation  @submit.prevent="validate">
              <v-list-item style="justify-content:center">
                <v-text-field
                  v-model="form.email"
                  :rules="[rules.requiredEmail, rules.validateEmail]"
                  disabled
                  name="email"
                  label="이메일"
                  id="email"
                  outlined
                  dense
                ></v-text-field>
              </v-list-item>
              <v-list-item style="justify-content:center">
                <v-text-field
                  v-model="form.password"
                  :append-icon="passwordValid ? 'mdi-eye' : 'mdi-eye-off'"
                  :rules="[rules.requiredPassword, rules.minLengthmax, rules.validatePassword, rules.hasSpace]"
                  :type="passwordValid ? 'text' : 'password'"
                  name="password"
                  label="비밀번호"
                  hint="영문, 숫자, 특수문자를 포함하여 8자 이상 입력해야합니다."
                  counter
                  @click:append="passwordValid = !passwordValid"
                  outlined
                  dense
                ></v-text-field>
              </v-list-item>
              <v-list-item style="justify-content:center">
                <v-text-field
                  v-model="form.passwordConfirm"
                  :append-icon="passwordValid ? 'mdi-eye' : 'mdi-eye-off'"
                  :rules="[rules.validateConfirm(form.password, form.passwordConfirm)]"
                  :type="passwordValid ? 'text' : 'password'"
                  name="passwordConfirm"
                  label="비밀번호 확인"
                  hint="비밀번호를 다시 한번 입력해주세요."
                  counter
                  @click:append="passwordValid = !passwordValid"
                  outlined
                  dense
                ></v-text-field>
              </v-list-item>
              <v-dialog v-model="termPopup" scrollable max-width="500px">
                <template v-slot:activator="{ on }">
                  <v-checkbox
                    v-model="form.isTerm"
                    readonly
                    label="약관에 동의합니다."
                    class="mt-0"
                    v-on="on"
                  ></v-checkbox>
                </template>
                <v-card dark color="#110b15">
                  <v-card-title>개인정보 제공 및 이용약관 동의</v-card-title>
                  <v-divider></v-divider>
                  <v-card-text style="height: 300px;">이용약관 내용</v-card-text>
                  <v-divider></v-divider>
                  <v-btn
                    color="#71d087"
                    class="blue-grey--text text--darken-4"
                    @click="termAgree"
                  >동의</v-btn>
                  <v-btn @click="termDeny">취소</v-btn>
                </v-card>
              </v-dialog>
              <v-list-item style="justify-content:center">
                <v-btn
                  @click="validate"
                  @keyup.enter="validate"
                  width="100%"
                  :disabled="!valid || !isSubmit"
                  color="#71d087"
                  class="blue-grey--text text--darken-4"
                >
                  회원가입
                  <v-icon>mdi-account-check</v-icon>
                </v-btn>
              </v-list-item>
                 </v-form>
            </v-list>
          </v-col>
        </v-row>
        <v-alert v-model="isFail" type="warning" dismissible class="py-2 my-3">회원가입 실패</v-alert>
        <v-alert v-model="isSuccess" type="success" dismissible class="py-2 my-3">회원가입 성공</v-alert>
      </v-container>
 
  </v-card>
</template>

<script>
import "../../assets/css/style.scss";
import "../../assets/css/user.scss";
import PV from "password-validator";
import * as EmailValidator from "email-validator";
import UserApi from "../../apis/UserApi";
export default {
  created() {
    if (this.$store.form) {
      this.form.email = this.$store.form.email;
      this.form.nickName = this.$store.form.nickName;
      this.$store.form = null;
    }
    this.passwordSchema
      .is()
      .min(8)
      .is()
      .max(20)
      .has()
      .digits()
      .has()
      .letters()
      .has()
      .symbols()
      .has()
      .not()
      .spaces();

    let URL = document.location.href;
    this.form.email = URL.split("/")[5].split("+")[1];
    this.form.key = URL.split("/")[5].split("+")[0];
  },
  data: () => {
    return {
      // 입력된 form 데이터
      isOkay: false,
      form: {
        // 미리 입력된 데이터
        key: "",
        email: "",

        // 직접 입력하도록
        nickName: "",
        password: "",
        passwordConfirm: "",
        isTerm: false
      },

      // 비밀번호를 확인할 수 있도록 하는
      passwordValid: false,

      // 비밀번호 규칙
      passwordSchema: new PV(),

      // 요청 보낼 때 확인하기 위한 값
      error: {
        email: null,
        password: null,
        nickName: null,
        passwordConfirm: null,
        term: null
      },

      // error의 값들이 모두 false일 경우, 버튼 활성화를 위한 값
      isSubmit: false,
      valid: false,

      // 약관 modal을 켜기 위한 스위치
      termPopup: false,

      // 회원가입 실패를 알려주기 위한 장치
      isFail: false,
      isSuccess: false,

      // 정보 입력시 유효한 데이터인지 검사
      rules: {
        limitLength: value => value.trim().length < 20 || "너무 길어요",
        validateKorean: v =>
          !/[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/.test(v) || "한글을 제외하고 입력해주세요.",
        requiredNickname: value => !!value || "별명을 입력해주세요.",
        requiredEmail: value => !!value || "이메일을 입력해주세요.",
        requiredPassword: value => !!value || "비밀번호를 입력해주세요.",
        emailMatch: () => "The email and password you entered don't match",
        minLengthmax: v =>
          (v.length >= 8 && v.length <= 20 && !/\s/.test(v)) ||
          "비밀번호는 공백없이 8자 이상 20자 이하 입력해야합니다.",
        validateEmail: v =>
          /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/.test(
            v
          ) || "이메일 형식을 지켜주세요.",
        validatePassword: v =>
          /^.*(?=^.{8,}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[`~!@#$%^&+=;',.?]).*$/.test(
            v
          ) || "영문, 숫자, 특수문자를 포함하여 공백없이 입력해주세요.",
        hasSpace: v => !/\s/.test(v) || "공백없이 입력해주세요.",
        validateConfirm: (v1, v2) =>
          v1 === v2 || "비밀번호가 일치하지 않습니다."
      }
    };
  },
  methods: {
    isValidNickname() {
      let temp = this.form.nickName.replace(/(\s*)/g, "");
      this.form.Nickname = temp;
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
    validate() {
      if (this.$refs.form.validate()) {
        // this.snackbar = true;
        if (this.isOkay) {
          this.isSubmit = true;
          this.join();
        } else {
          alert("닉네임에 ✔️를 만들어주세요 !");
        }
      }
    },
    termAgree() {
      this.form.isTerm = true;
      this.termPopup = false;
    },
    termDeny() {
      this.form.isTerm = false;
      this.termPopup = false;
    },
    windowClose() {
      window.open("", "_self").close();
    },
    checkForm() {
     if (this.form.email && !EmailValidator.validate(this.form.email)) {
        this.error.nickName = false;
        this.error.email = "이메일을 확인해주세요.";
        return "이메일을 확인해주세요.";
      } else if (
        this.form.password &&
        !this.passwordSchema.validate(this.form.password)
      ) {
        this.error.email = false;
        this.error.password =
          "비밀번호는 영문, 숫자, 특수문자를 포함하여 8자 이상 20자 이하여야 합니다.";
        return "비밀번호는 영문, 숫자, 특수문자를 포함하여 8자 이상 20자 이하여야 합니다.";
      } else if (
        this.form.passwordConfirm &&
        this.form.password !== this.form.passwordConfirm
      ) {
        this.error.password = false;
        this.error.passwordConfirm = "비밀번호가 일치하지 않습니다.";
        return "비밀번호가 일치하지 않습니다.";
      } else if (!this.form.isTerm) {
        this.error.passwordConfirm = false;
        this.error.term = "약관에 동의해야합니다.";
        return "약관에 동의해야합니다.";
      } else {
        this.error.email = false;
        this.error.password = false;
        this.error.passwordConfirm = false;
        this.error.term = false;
        return false;
      }
    },
    join() {
      if (
        !this.error.email &&
        !this.error.password &&
        !this.error.passwordConfirm &&
        this.form.isTerm
      ) {
        let joinForm = {
          username: this.form.email,
          email: this.form.email,
          nickname: this.form.nickName,
          password: this.form.password,
          key: this.form.key
        };
        this.$store.form = joinForm;
        UserApi.requestSignup(
          joinForm,
          response => {
            this.isSuccess = response.data.message;
            setTimeout(() => {
              this.isSuccess = false;
              this.windowClose();
            }, 2000);
          },
          error => {
            this.isFail = true;
            setTimeout(() => {
              this.isFail = false;
            }, 2000);
          }
        );
        //----------------------------------------
        // 회원가입을 위해 back으로 추가정보 전송
        // router.push({name: '이메일 인증'})
        //----------------------------------------
      } else if (this.error.nickName) {
        alert("닉네임을 다시 확인해주세요.");
      } else if (this.error.email) {
        alert("이메일을 다시 확인해주세요.");
      } else if (this.error.password || this.error.passwordConfirm) {
        alert("비밀번호를 다시 확인해주세요.");
      } else if (!this.form.isTerm) {
        alert("약관에 동의해주세요.");
      }
    }
  },
  watch: {
    form: {
      deep: true,
      handler() {
        // this.validate();
        let check = this.checkForm();
        if (check) {
          alert('한번 더 확인해주세요.')
        } else {
          this.isSubmit = true;
        }
      }
    }
  }
};
</script>
