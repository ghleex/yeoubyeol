<template>
  <v-card dark color="#110b22">
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-container fluid class="py-3">
        <v-row no-gutters justify="space-between" align="center">
          <v-col cols="12" class="pt-2">
            <h1>가입할 때 사용한</h1>
            <h1>이메일을 입력해주세요.</h1>
            <h1>임시비밀번호를 보내드림다.</h1>
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
              @click="sendEmailPW"
              :disabled="!valid"
            >이메일 전송</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </v-card>
</template>

<script>
<<<<<<< HEAD
import JoinApi from "../../apis/JoinApi";
import axios from "axios";
export default {
  created() {
    if (this.$store.emailPW) {
      this.email = this.$store.emailPW;
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
  }),
  methods: {
    sendEmailPW() {
      var router = this.$router;
      //   console.log(this.email);
      JoinApi.sendEmailPW(
        this.email,
        res => {
          console.log(res);
          //성공 시
          if (res.status === 200) {
            this.$store.emailPW = this.email;
            router.push({
              path: "/user/password/ok"
            });
          } //이미 있는 이메일인 경우
          else if (res.status === 202) {
            this.message = res.data.message;
            this.alert = true;
            this.valid = false;
          }
=======
    // import ButtonCustom from '../../components/common/ButtonCustom'
    import emailjs from 'emailjs-com';
    import * as EmailValidator from 'email-validator';
    import axios from 'axios';
    export default {
        components: {
            // ButtonCustom,
        },
        created() {
            if (this.$store.email) {
                this.email = this.$store.email
                if (this.checkForm()) {
                    this.isSubmit = true
                }
                this.$store.email = null
            }
        },
        data: () => {
            return {
                email: '',
                error: {
                    email: false,
                },
                isSubmit: false,
            }
        },
        methods: {
            checkForm() {
                if (this.email.length >= 0 && !EmailValidator.validate(this.email)) {
                    this.error.email = "이메일 형식이 아닙니다."
                    console.log('hi')
                    return false
                } else {
                    this.error.email = false;
                    console.log('bye')
                    return true
                }
            },
            sendEmail() {
                var router = this.$router
                console.log(this.email)
                if (this.email && !this.error.email) {
                    this.$store.email = this.email
                    router.push({
                        path: '/user/password/ok'
                    })
                let form = new FormData();
                form.append('username', this.email)
                axios.post('http://192.168.31.80:8000/accounts/find_pwd/', form)
                .then(response => {
                    console.log(response)
                })
                }
            },
        },
        watch: {
            email: function (v) {
                this.checkForm();
            },
            error: {
                deep: true,
                handler() {
                    if (!this.error.email) {
                        this.isSubmit = true
                    } else {
                        this.isSubmit = false
                    }
                }
            }
>>>>>>> 41bd4035c54303915650898ddbba921f3e5c78d8
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
      this.sendEmailPW();
    }
  }
};
</script>