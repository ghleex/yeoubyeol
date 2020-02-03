<template>
  <v-card dark color="#110b22">
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-container fluid class="py-3">
        <v-row no-gutters justify="space-between" align="center">
          <v-col cols="12" class="pt-2">
            <h1>가입할 때 사용할</h1>
            <h1>이메일을 입력해주세요.</h1>
            <h1>함께할 초대장을 보내드림다.</h1>
          </v-col>
          <v-col cols="12" class="pt-5">
            <v-text-field
              outlined
              v-model="email"
              :rules="emailRules"
              label="이메일"
              hint="이메일입력 필수"
              required
            ></v-text-field>
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
              @click="sendEmail"
              :disabled="!valid"
            >이메일 전송</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </v-card>
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
      var router = this.$router;
      //   console.log(this.email);
      JoinApi.JoinsendEmail(
        this.email,
        res => {
          console.log(res);
          //성공 시
          if (res.status === 200) {
            this.$store.email = this.email;
            router.push({
              path: "/join/ok1"
            });
          } //이미 있는 이메일인 경우
          else if (res.status === 202) {
            this.message = res.data.message;
            this.alert = true;
            this.isSubmit = false;
            this.valid = false;
          }
        },
        error => {
          //에러
          console.log(error);
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