<template>
  <div class="wrapC">
      <h1 style="color: #EEEEEE;">
        입력하신 메일로 <br>
        링크 보내드렸어요 <br>
      </h1>
      <h1>
        <br>
        메일을 확인해보세요 <br>
        &lt; {{ email }} &gt;
      </h1>
      <div class="remail-home-button">
          <button
            style="border: 1px solid #FFDD77;"
            class="email-backward"
            @click="backward">
              메일이 도착하지 않았나요?
          </button>
          <button class="orange"
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
    created() {
      this.email = this.$store.email
    },
    methods: {
      backward() {
        var router = this.$router
        router.push({
          name: '비밀번호 변경',
        })
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