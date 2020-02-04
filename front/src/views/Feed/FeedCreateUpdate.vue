<template>
  <div>
    <v-card dark color="#110b22">
      <v-form ref="form" v-model="valid" lazy-validation>
        <v-row class="py-0 ma-2">
          <v-col cols="12" class="pa-1">
            <v-file-input accept="image/*"></v-file-input>
            <!-- <v-text-field dark label="홍주의 미니랩실" required></v-text-field> -->
          </v-col>

          <v-col cols="12" class="pa-1">
            <v-textarea 
                dark 
                :rules="contentRules" 
                required 
                outlined 
                :value="inputPostContent">
            </v-textarea>
            <v-btn
              block
              class="mb-2"
              color="#71d087"
              style="color:#110b22"
              @click="validate"
              :disabled="!valid"
            >피드 발행하기</v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-card>
  </div>
</template>

<script>
import FeedApi from '@/apis/FeedApi'

export default {
    methods: {
        validate() {
            if (this.$refs.form.validate()) {
            // this.snackbar = true;
                this.newPost();
            }
        },
        newPost() {
            let data = new FormData();
            data.append('nickname', this.loginedNickname);
            data.append('article', 'my-picture');
            data.append('image', event.target.files[0]); 

            FeedApi.newPost(data,res=>{

            })
        },
    }

};
</script>

<style>
</style>