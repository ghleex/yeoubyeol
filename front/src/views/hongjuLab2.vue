<template>
  <div style="position:fixed">
    <div class="js-weather weather" style="background-color:#fff">
      <h1>어서오세요 홍주의 랩실 2 는 타이머 입니당</h1>
      <h3>{{ target }}</h3>
      <h3>{{ curr }}</h3>
      <h3 id="lastTime">{{ lastTime }}</h3>
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
    updateTransition(time) {
      var el = document.querySelector("#lastTime");
      
      if (time === 11) {
        el.className = "last_time1";
      } else {
        el = document.querySelector("#lastTime");
        el.className = "last_time2";
      }
      
      return el;
    },
    getTime() {
      const now = new Date();
      const hours = now.getHours();
      const minutes = now.getMinutes();
      const seconds = now.getSeconds();
      this.curr = `${hours < 10 ? `0${hours}` : hours}시
      ${minutes < 10 ? `0${minutes}` : minutes}분
      ${seconds < 10 ? `0${seconds}` : seconds}초`;
      
      if (hours === 22 && minutes === 50 && seconds === 0) {
        this.updateTransition(11)
      } else if (hours === 4 && minutes === 50 && seconds === 0) {
        this.updateTransition(5)
      }

      const baseTime = new Date();
      let newDate = baseTime.getDate() + 1
      if (hours >= 5) {
        baseTime.setDate(newDate)
      }
      baseTime.setHours(5)
      baseTime.setMinutes(0)
      baseTime.setSeconds(0)

      const diffTime = (baseTime - now) / 1000;
      let lastHours = diffTime / 3600;
      if (0 <= lastHours && lastHours < 10) {
        lastHours = `0${Math.floor(lastHours)}`;
      } else if (lastHours < 0 || isNaN(lastHours)) {
        lastHours = '00';
      } else {
        lastHours = Math.floor(lastHours);
      }
      
      let lastMinutes = diffTime % 3600 / 60;
      if (0 <= lastMinutes && lastMinutes < 10) {
        lastMinutes = `0${Math.floor(lastMinutes)}`;
      } else if (lastMinutes < 0 || isNaN(lastMinutes)) {
        lastMinutes = '00';
      } else {
        lastMinutes = Math.floor(lastMinutes);
      }

      let lastSeconds = diffTime % 3600 % 60;
      if (0 <= lastSeconds && lastSeconds < 10) {
        lastSeconds = `0${Math.floor(lastSeconds)}`;
      } else if (lastSeconds < 0 || isNaN(lastSeconds)) {
        lastSeconds = '00';
      } else {
        lastSeconds = Math.floor(lastSeconds);
      }

      const lastTime = `${lastHours}:${lastMinutes}:${lastSeconds}`
      this.lastTime = lastTime
    }
  }
};
</script>

<style scope>
.last_time1 {
  background-color: #110B22;
  color: #fff;
  -webkit-transition-property: background-color -webkit-transform color;
  -webkit-transition-duration: 300s;
  -webkit-transition-timing-function: ease-in-out;
  transition-property: background-color -webkit-transform color;
  transition-duration: 300s;
  transition-timing-function: ease-in-out;
}

.last_time2 {
  background-color: #042889;
  color: #ef8949;
  -webkit-transition-property: background-color -webkit-transform color;
  -webkit-transition-duration: 300s;
  -webkit-transition-timing-function: ease-in-out;
  transition-property: background-color -webkit-transform color;
  transition-duration: 300s;
  transition-timing-function: ease-in-out;
}
</style>