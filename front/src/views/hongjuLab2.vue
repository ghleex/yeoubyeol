<template>
  <div  style="position:fixed">
    <div>
      <div class="js-weather weather" style="background-color:#fff">
        <h1> 어서오세요 홍주의 랩실 2 는 날씨 API 입니당</h1>
        {{ data }}
        <h2>{{data1}}</h2>
        <v-img src="http://openweathermap.org/img/w/02n.png"  max-width=40 max-height=40>

        </v-img>
        <span class="weather__text"></span>

        <v-btn @click="setClear()">clear</v-btn>
        <v-btn @click="loadWeather()">get</v-btn>
      </div>
    </div>
    <v-progress-circular
      indeterminate
      color="primary"
    ></v-progress-circular>

    <v-progress-circular
      indeterminate
      color="red"
    ></v-progress-circular>

    <v-progress-circular
      indeterminate
      color="purple"
    ></v-progress-circular>

    <v-progress-circular
      indeterminate
      color="green"
    ></v-progress-circular>

    <v-progress-circular
      indeterminate
      color="amber"
    ></v-progress-circular>
  </div>
</template>
    <script>
const API_KEY = "241051bf13976dd3ddf8b8d9f247255e";
const WEATHER_API = "https://api.openweathermap.org/data/2.5/weather?";

export default {
  data() {
    return {
      data: "",
      data1: "",
      icon:'',
    };
  },

  created() {
    this.loadWeather();
  },
  methods: {
    setClear() {
      localStorage.removeItem("coords");
      this.data='';
      this.data1='';
    },
    getWeather(coords) {
      fetch(
        `${WEATHER_API}lat=${coords.lat}&lon=${coords.lng}&appid=${API_KEY}&units=metric`
      )
        .then(response => response.json())
        .then(json => {
          const name = json.name;
          const temperature = json.main.temp;
          console.log(json);
          this.data = json;
          this.icon=json.weather.icon;
          this.data1 = `${Math.floor(temperature)}° @ ${name}`;
        });
    },

    handleGeoSuccess(position) {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;
      const coords = {
        lat,
        lng
      };
      localStorage.setItem("coords", JSON.stringify(coords));
      this.getWeather(coords);
    },

    handleGeoFailure() {
      console.log("no location");
    },

    loadWeather() {
      const currentCoords = localStorage.getItem("coords");
      if (currentCoords !== null) {
        const parsedCoords = JSON.parse(currentCoords);
        this.getWeather(parsedCoords);
        return;
      } else {
        navigator.geolocation.getCurrentPosition(
          this.handleGeoSuccess,
          this.handleGeoFailure
        );
      }
    }
  }
};
</script>

<style scoped>
.v-progress-circular {
  margin: 1rem;
}
</style>
