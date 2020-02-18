<template>
  <v-card dark color="#110b22">
    <v-container fluid class="py-3">
      <v-row no-gutters justify="space-between" align="center">
        <v-col cols="12" class="pt-2">
          <h1 style="color: #EEEEEE;">
            입력하신 메일로
            <br />임시비밀번호를 보내드렸어요
            <br />
          </h1>
          <h1>
            <br />메일을 확인해보세요
            <br />
            &lt; {{ email }} &gt;
          </h1>
        </v-col>

        <v-col cols="12" style="margin-top:200px;">
            <v-btn text block @click="backward">메일이 도착하지 않았나요?</v-btn>
            <v-btn
              min-height="50"
              color="#71d087"
              style="color:#110b22;"
              block
              class="confirm"
              @click="toLogin"
            >로그인 화면으로</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
export default {
  created() {
    this.email = this.$store.emailPW;
  },
  methods: {
    backward() {
      let router = this.$router;
      router.push({
        name: "비밀번호 변경"
      });
    },
    toLogin() {
      let router = this.$router;
      router.push({ name: "로그인" });
    }
  }
};
</script>

<style>
</style>