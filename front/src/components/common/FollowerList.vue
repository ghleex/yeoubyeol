<template>
  <v-card dark color="#110b22">
    <v-card-actions class="px-0">
      <v-list-item class="grow px-2 py-0">
        <v-list-item-avatar color="grey darken-3">
          <v-img class="elevation-6" :src="getPic"></v-img>
        </v-list-item-avatar>

        <v-list-item-content @click="changeViewProfile('프로필',nickName)">
          <v-list-item-title style="color:#71d087">{{nickName}}</v-list-item-title>
          {{intro}}
        </v-list-item-content>

        <v-col align="center" justify="end" cols="4" v-if="isMyAccount">
          <span class="subheading grey--text px-2">
            <v-btn v-if="isFollowing" text style="color:#71d087">팔로잉 취소</v-btn>
            <v-btn v-else text style="color:#71d087">팔로잉</v-btn>
          </span>
        </v-col>
      </v-list-item>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    intro: {
      type: String,
      default: " "
    },
    nickName: {
      type: String,
      default: "default"
    },
    picName: {
      type: String,
      default: "0"
    },
    isFollowing: {
      type: Boolean,
      default: false
    },
    isMyAccount: {
      type: Boolean,
      default: false
    }
  },
  data: function() {
    return {
      getPic: ""
    };
  },
  methods: {
    changeViewProfile(path, usersEmail) {
      this.pageTitle = usersEmail;
      this.$router.push({ name: path, params: { email: usersEmail } });
    }
  },
  created() {
    this.getPic = require("@/assets/images/profile/" + this.picName + ".png");
  }
};
</script>
