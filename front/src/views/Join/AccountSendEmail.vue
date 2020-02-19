<template>
  <v-responsive fluid class="py-3">
    <v-form ref="form" v-model="valid" lazy-validation v-on:submit.prevent="sendEmail">
      <v-row class="pt-2 mx-2" align="start" justify="center">
          
        <v-col cols="12" class="pt-6">
          <v-card dark color="#110b22">
            <h1>가입할 때 사용할</h1>
            <h1>이메일을 입력해주세요.</h1>
            <h1>함께할 초대장을 보내드림다.</h1>
            <div class="py-2"></div>
            <v-text-field
              outlined
              v-model="email"
              :rules="emailRules"
              label="이메일"
              hint="이메일입력 필수"
              required
            ></v-text-field>
          </v-card>
        </v-col>
        <v-col cols="12" style="margin-top:200px;">
          <v-alert
            v-model="alert"
            dismissible
            type="warning"
            color="#F15050"
            class="py-2"
          >{{message}}</v-alert>
          <v-btn
            min-height="50"
            color="#71d087"
            style="color:#110b22;"
            block
            class="confirm"
            @click.prevent="sendEmail"
            :disabled="!valid"
          >이메일 전송</v-btn>
             <v-progress-linear
              :active="loading"
              :indeterminate="loading"
              absolute
              bottom
              color="green"
            ></v-progress-linear>
        </v-col>
      </v-row>
    </v-form>
  </v-responsive>
</template>

<script>
import JoinApi from "../../apis/JoinApi";
import axios from "axios";
export default {
  created() {
    if (this.$store.email) {
      this.email = this.$store.email;
    }
  },
  data: () => ({
    loading: false,
    message: "",
    alert: false,
    valid: false,
    email: "",
    emailRules: [
      v => !!v || "이메일 형식이 아닙니다.",
      v => /.+@.+\..+/.test(v) || "이메일 형식이 아닙니다."
    ],
    error: {
      email: false
    },
    isSubmit: false
  }),
  methods: {
    sendEmail() {
      let router = this.$router;
        this.loading=true;
      JoinApi.JoinsendEmail(
        this.email,
        res => {
          //성공 시
          if (res.status === 200) {
            this.$store.email = this.email;
            router.push({
              path: "/join/ok"
            });
          } //이미 있는 이메일인 경우
          else if (res.status === 202) {
            this.message = res.data.message;
            this.alert = true;
            this.isSubmit = false;
            this.valid = false;
            this.loading=false;
          }
        },
        error => {
          //에러
          this.loading=false;
          router.push({ path: "/error" });
        }
      );
    }
  },
  validate() {
    if (this.$refs.form.validate()) {
      this.isSubmit = true;
      this.sendEmail();
    }
  }
};
</script>