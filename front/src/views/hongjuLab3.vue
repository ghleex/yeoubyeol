<template>
  <div style="position:fixed">
    <div class="js-weather weather" style="background-color:#fff">
      <h1>어서오세요 홍주의 랩실 2 는 타이머 입니당</h1>
        <v-btn
              min-height="50"
              color="#71d087"
              style="color:#110b22;"
              block
              class="confirm"
            >이메일 전송</v-btn>
      <v-progress-linear
        :active="loading"
        :indeterminate="loading"
        absolute
        bottom
        color="deep-purple accent-4"
      ></v-progress-linear>

    </div>
  </div>
</template>
    <script>
export default {
  data() {
    return {
      loading:true,
    };
  }
};
</script>
