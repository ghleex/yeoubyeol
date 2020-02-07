<template>
  <v-container>
    <h1 class="white--text">어서오세용 홍주의 랩실3에서는 아이콘변경 / 파일 업로드 입니당.</h1>
    <div class="white">
      <label>
        File
        <div id="preview">
          <img v-if="url" :src="url" />
        </div>
        <v-file-input
          accept="image/*"
          prepend-icon="mdi-camera"
          outlined
          dense
          label="Image"
          @change="onFileChanged"
        ></v-file-input>
      </label>
      <v-btn v-on:click="submitFile()">Submit</v-btn>
    </div>
    <h2 class="grey--text">---------- 절취선 ----------</h2>
    <div class="white">
      <v-text-field v-model="name" label="file name" solo-inverted></v-text-field>
      <v-btn @click="setFileName">click</v-btn>
      <v-avatar>
        <img :src="test" alt="John" />
      </v-avatar>

      <v-avatar>
        <img src="../assets/images/profile_default.png" alt="John" />
      </v-avatar>
    </div>
  </v-container>
</template>

<script>
import axios from "axios";
export default {
  /*
      Defines the data used by the component
    */
  data() {
    return {
      file: "",
      source: "profile_default.png",
      name: "",
      test: "",
      url: null
    };
  },

  methods: {
    /*
        Submits the file to the server
      */
    submitFile() {
      /*
                Initialize the form data
            */
      let formData = new FormData();

      /*
                Add the form data we need to submit
            */
      formData.append("file", this.file);

      /*
          Make the request to the POST /single-file URL
        */
      axios
        .post(`http://192.168.31.87:8000/articles/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(function() {
          console.log("SUCCESS!!");
        })
        .catch(function() {
          console.log("FAILURE!!");
        });
    },

    /*
        Handles a change on the file upload
      */
    onFileChanged(event) {
      this.file = event;
      console.log(this.file);
      this.url = URL.createObjectURL(this.file);
    },
    setFileName() {
      this.source = this.name;
      // console.log(this.setBG);
      this.test = require("../assets/images/" + this.source);
      console.log(this.test);
    },
    setBG() {
      return `@/assets/images/${this.source}`;
    }
  }
};
</script>

<style scoped>
#preview {
  display: flex;
  justify-content: center;
  align-items: center;
}

#preview img {
  max-width: 100%;
  max-height: 500px;
}
</style>
