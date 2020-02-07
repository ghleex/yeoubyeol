<template>
  <div>
    <v-card dark color="#110b22">
      <v-form ref="form" v-model="valid" lazy-validation>
        <v-row class="py-0 ma-2">
          <v-col cols="12" class="pa-1">
            <v-file-input accept="image/*" @change="onFileChanged"></v-file-input>
          </v-col>

          <v-col cols="12" class="pa-1">
            <v-textarea
              dark
              :rules="contentRules"
              required
              outlined
              v-model="inputPostContent"
              :autofocus="true"
              :auto-grow="true"
              clearable
            >{{inputPostContent}}</v-textarea>
            <v-btn
              block
              class="mb-2"
              color="#71d087"
              style
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
import FeedApi from "@/apis/FeedApi";

export default {
  created() {
    this.loginedNickname= JSON.parse(
      sessionStorage.getItem("LoginUserInfo")
    ).nickname;
  },
  methods: {
    onFileChanged(event) {
      console.log(this.$refs)
      this.selectedFile = this.$refs.selectedFile.files[0]
    },
    validate() {
      if (this.$refs.form.validate()) {
        // this.snackbar = true;
        this.newPost();
      }
    },
    newPost() {
  let form = new FormData();
    form.append("nickname", this.loginedNickname);
    form.append("article", this.inputPostContent);
    form.append("image", this.selectedFile);
    console.log(typeof(this.selectedFile));
      FeedApi.newPost(
        form,
        res => {
          console.log(res);
        },
        error => {
          console.log("error");
        }
      );
    }
  },
  data: () => {
    return {
      loginedNickname: "",
      selectedFile: "",
      inputPostContent: "",
      valid: false,
      contentRules: [v => !!v || "내용을 입력해주세요.."]
    };
  }
};
</script>

<style>
</style>