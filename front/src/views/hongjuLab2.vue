<template>
  <div>
 <v-text-field
            v-model="name"
            label="file name"
            solo-inverted
          ></v-text-field>
    <v-btn @click="setFileName">click</v-btn>
   <v-avatar>
      <img
        :src="test"
        alt="John"
      >
    </v-avatar>
  
   <v-avatar>
      <img
        src="../assets/images/profile_default.png"
        alt="John"
      >
    </v-avatar>

  </div>
</template>

<script>

export default {

  data: () => ({
    source:'profile_default.png',
    name:'',
    test:"",
  }),
  methods: {
    setFileName(){
      // this.source = this.name;
      // console.log(this.setBG);
      this.test = require('../assets/images/'+this.source);
      console.log(this.test);

    },
     setBG(){
      return `@/assets/images/${this.source}`;
    }
  },
  created() {
  },
};
</script>

