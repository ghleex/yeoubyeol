<template>
  <v-container>
    <div class="large-12 medium-12 small-12 cell">
      <label>File
        <v-file-input id="file" ref="file" v-on:change="handleFileUpload()"/>
      </label>
      <v-btn v-on:click="submitFile()">Submit</v-btn>
    </div>
  </v-container>
</template>

<script>
import axios from 'axios';
  export default {
    /*
      Defines the data used by the component
    */
    data(){
      return {
        file: ''
      }
    },

    methods: {
      /*
        Submits the file to the server
      */
      submitFile(){
        /*
                Initialize the form data
            */
            let formData = new FormData();

            /*
                Add the form data we need to submit
            */
            formData.append('file', this.file);

        /*
          Make the request to the POST /single-file URL
        */
            axios.post( `http://192.168.31.80:8000/articles/`,
                formData,
                {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
              }
            ).then(function(){
          console.log('SUCCESS!!');
        })
        .catch(function(){
          console.log('FAILURE!!');
        });
      },

      /*
        Handles a change on the file upload
      */
      handleFileUpload(){
        this.file = this.$refs.file.files[0];
      }
    }
  }
</script>