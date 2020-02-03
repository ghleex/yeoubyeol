<template>
  <div class="wrapC error">
    <div class="div-flex">
      <div class="errormark">
        <h1>
          E <br>
          R <br>
          R <br>
          O <br>
          R <br>
        </h1>
      </div>
      <div class="errormessage">
        <h2>
          죄송합니다 <br>
          여유를 가지고 <br>
          다시 해주세요
        </h2>
      </div>
    </div>
    <button @click="backward">
      이전으로
    </button>
  </div>
</template>

<script>
import '../../assets/css/errorpage.scss'
export default {
  data: () => {
    return {
      
    }
  },
  methods: {
    backward() {
      var router = this.$router
      router.go(-1)
    }
  }
}
</script>

<style>

</style>