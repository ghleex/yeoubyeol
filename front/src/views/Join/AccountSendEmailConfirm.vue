<template>
  <div class="wrapC">
      <h1 style="color: #EEEEEE;">
        입력하신 메일로 <br>
        링크 보내드렸어요 <br>
      </h1>
      <h1>
        <br>
        메일을 확인해보세요 <br>
        {{ email }}
      </h1>
      <div class="remail-home-button">
          <button
            class="email-backward"
            @click="backward">
              메일이 도착하지 않았나요?
          </button>
          <button class="base"
            style="height: 50px;
                   border-radius: 5px;"
            @click="toLogin">
              로그인 화면으로
          </button>
      </div>
  </div>
</template>

<script>
export default {
  data: () => {
    return {
      email: ''
    }
  },
  created() {
    console.log(this.$store.state.form)
    this.email = this.$store.state.form.email
  },
  methods: {
    backward() {
      var router = this.$router
      router.push({ name: '인증메일 발송' })
    },
    toLogin() {
      var router = this.$router
      router.push({name: '로그인'})
    }
  }
}
</script>

<style>

</style>