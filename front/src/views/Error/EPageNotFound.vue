<template>
  <div class="wrapC pagenotfound">
    <div>
      <div>
        <h1>
          Page <br>
          Not <br>
          Found <br>
        </h1>
      </div>
      <h1>
        <br> 모든 걸 찾을 수는 없어요.
      </h1>
    </div>
    <button @click="toHome">
      처음으로
    </button>
  </div>
</template>

<script>
import '../../assets/css/errorpage.scss'
export default {
  methods: {
    toHome() {
      let router = this.$router
      router.push({name: '홈'})
    }
  }
}
</script>

<style>

</style>