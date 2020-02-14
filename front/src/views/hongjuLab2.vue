<template>
  <div style="position:fixed">
    <div class="js-weather weather" style="background-color:#fff">
      <h1>어서오세요 홍주의 랩실 2 는 타이머 입니당</h1>
      <h3>target : {{ target }}</h3>
      <h3>curr : {{ curr }}</h3>
      <h3 v-if="!isOver">lastTime : {{lastTime }}</h3>
      <h3 v-else class="red--text">작성 가능한 시간이 아니에요</h3>
    </div>
  </div>
</template>
    <script>
export default {
  data() {
    return {
      data: "",
      curr: "",
      target: "",
      timer: "",
      lastTime: "",
      isOver:false,
    };
  },

  created() {
    let today = new Date();
    this.target = new Date();
    // if (today.getHours() <= 5 && today.getHours() > -1) {
    // if (today.getHours() <= 5 && today.getHours() > -1) {
    if (today.getMinutes() <= 5 && today.getMinutes() > -1) {
      this.target = today;
      this.target.setHours(5);
      this.target.setMinutes(0);
      this.target.setSeconds(0);
      // } else if (today.getHours() >= 23) {
      // } else if (today.getHours() >= 23) {
    } else if (today.getMinutes() >= 23) {
      this.target = today;
      this.target.setDate(today.getDate() + 1);
      this.target.setHours(5);
      this.target.setMinutes(0);
      this.target.setSeconds(0);
    }

    this.getTime();
 /*    setInterval(() => {
      this.getTime();
    }, 1000); */
  },
  methods: {
    getTime() {
      const now = new Date();
      const hours = now.getHours();
      const minutes = now.getMinutes();
      const seconds = now.getSeconds();
      this.isOver = false;
      this.curr = `${hours < 10 ? `0${hours}` : hours}:${
        minutes < 10 ? `0${minutes}` : minutes
      }:${seconds < 10 ? `0${seconds}` : seconds}`;

      const lasthours = Math.ceil(
        (this.target.getTime() - now.getTime()) / 1000 / 60 / 60
      );
      const lastminutes = Math.ceil(
        (this.target.getTime() - now.getTime()) / 1000 / 60
      );
      const lastseconds = Math.ceil(
        (this.target.getTime() - now.getTime()) / 1000
      );
      console.log(lasthours<1);
      console.log(lastminutes<1);
      console.log(lastseconds<1);
      if(lasthours<1 && lastminutes<1 && seconds <1){
        this.isOver= true;
      }

      this.lastTime = `
      ${lasthours < 10 ? `0${lasthours}` : lasthours}:
      ${lastminutes < 10 ? `0${lastminutes}` : lastminutes}:
      ${lastseconds < 10 ? `0${lastseconds}` : lastseconds}`;
    }
  }
};
</script>
