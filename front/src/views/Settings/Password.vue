<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <v-col cols="12" class="py-0">
        <v-list dark color="#110B22">
          <v-list-item style="justify-content:center">
            <v-btn text dark small @click="backToProfileSetting">취소</v-btn>
            <v-spacer></v-spacer>
            <v-btn
              text
              dark
              small
              :disabled="!valid"
              v-show="isConfirm"
              @click="validate"
              color="#71D087"
            >저장</v-btn>
            <br />
          </v-list-item>
          <v-list-item style="justify-content:center">
            <v-divider></v-divider>
          </v-list-item>
          <v-form
            ref="form"
            v-model="valid"
            lazy-validation
            v-if="!isConfirm"
            @submit.prevent="validate"
          >
            <v-list-item style="justify-content:center">
              <v-text-field
                label="현재 비밀번호"
                v-model="currPwd"
                dark
                type="password"
                counter
                outlined
                dense
                required
                :rules="[rules.requiredPassword, rules.minLengthmax, rules.validatePassword, rules.hasSpace]"
              ></v-text-field>
            </v-list-item>
            <v-list-item>
              <v-btn block outlined @click="validate">확인</v-btn>
            </v-list-item>
          </v-form>
          <v-form ref="form" v-model="valid" lazy-validation v-if="isConfirm">
            <v-list-item>
              <v-text-field
                v-model="form.password"
                :rules="[rules.requiredPassword, rules.minLengthmax, rules.validatePassword, rules.hasSpace]"
                type="password"
                name="password"
                label="새 비밀번호"
                hint="영문, 숫자, 특수문자를 포함하여 8자 이상 입력해야합니다."
                counter
                outlined
                dense
              ></v-text-field>
            </v-list-item>
            <v-list-item>
              <v-text-field
                v-model="form.passwordConfirm"
                :rules="[rules.validateConfirm(form.password, form.passwordConfirm)]"
                name="passwordConfirm"
                type="password"
                label="새 비밀번호 확인"
                hint="비밀번호를 다시 한번 입력해주세요."
                counter
                outlined
                dense
              ></v-text-field>
            </v-list-item>
          </v-form>
        </v-list>
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
  },
  data() {
    return {
      valid: false,
      isConfirm: false,
      loginedNickname: "",
      currPwd: "",
      form: {
        password: "",
        passwordConfirm: ""
      },

      rules: {
        requiredPassword: value => !!value || "비밀번호를 입력해주세요.",
        minLengthmax: v =>
          (v.length >= 8 && v.length <= 20 && !/\s/.test(v)) ||
          "비밀번호는 공백없이 8자 이상 20자 이하 입력해야합니다.",
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
    checkPassword() {
      let form = new FormData();
      form.append("password", this.currPwd);
      form.append("nickname", this.loginedNickname);
      UserApi.confirmPassword(
        form,
        res => {
          this.isConfirm = !this.isConfirm;
        },
        error => {
          alert("입력한 비밀번호가 틀렸습니다.");
        }
      );
    },
    backToProfileSetting() {
      this.$router.push({
        name: "프로필 변경",
        params: { email: this.loginedNickname }
      });
    },
    changePassword() {
      if (this.form.password === this.form.passwordConfirm) {
         let form = new FormData();
      form.append("password", this.form.password);
      form.append("nickname", this.loginedNickname);
        UserApi.editUserPassword(
          form,
          res => {
            alert("비밀번호가 변경되었어요 !");
            this.backToProfileSetting();
          },
          error => {
            alert("비밀번호 변경에 오류가 생겼어요 ..");
          }
        );
      } else {
        alert("새 비밀번호와 재입력이 다른 것 같아요 ..");
      }
    },
    validate() {
      if (this.$refs.form.validate()) {
        //저장하는 메소드 들어가야함
        if (!this.isConfirm) {
          this.checkPassword();
        } else {
          this.changePassword();
        }
      }
    }
  }
};
</script>

<style>
</style>