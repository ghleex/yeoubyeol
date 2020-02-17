<template>
    <div>
      <h1>어서오세요 홍주의 랩실 2 는 워드크라우드입니당</h1>
  <div>
      <wordcloud
      :data="defaultWords"
      nameKey="name"
      valueKey="value"
      color="Accent"
      spiral="rectangular"
      :showTooltip="true"
      :wordClick="wordClickHandler">
      </wordcloud>
    </div>
  </div>
</template>
    <script>
  import wordcloud from 'vue-wordcloud';
export default {
  components:{
   wordcloud
  },
    methods: {
    wordClickHandler(name, value, vm) {
      console.log('wordClickHandler', name, value, vm);
    }
  },
  data() {
    return {
      myColors: ['#1f77b4', '#629fc9', '#94bedb', '#c9e0ef'],
      defaultWords: [{
          "name": "Cat",
          "value": 26
        },
        {
          "name": "fish",
          "value": 19
        },
        {
          "name": "things",
          "value": 18
        },
        {
          "name": "look",
          "value": 16
        },
        {
          "name": "two",
          "value": 15
        },
        {
          "name": "fun",
          "value": 9
        },
        {
          "name": "know",
          "value": 9
        },
        {
          "name": "good",
          "value": 9
        },
        {
          "name": "play",
          "value": 6
        }
      ]
    }
  }
}
</script>