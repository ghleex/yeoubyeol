<template>
<div>
  <v-card
      class="mx-2"
      color="#110B22"
      dark
      outlined
      style="border: 1px solid #71d087;"
    >
      <v-list-item>
        <v-list-item-avatar color="grey darken-3">
          <v-img
            :src="pic_name"
          ></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>{{ nickname }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-card-text class="subtitle-2 grey--text text--lighten-5 pb-0">
        {{article}}
        <br>
        <v-row class="overline font-weight-thin pr-4" align="center" justify="end">
          2시간 전
        </v-row>
      </v-card-text>
  
      <v-card-actions class="pt-0">
        <v-list-item>
          <v-row
            class="mr-1"
            align="center"
            justify="end"
          >
            <a href="#" @click.prevent="iLoveIt">
              <v-icon class="mr-1" size="x-large" v-if="!isLike">mdi-heart-outline</v-icon>
              <v-icon class="mr-1" size="x-large" color="red" v-if="isLike">mdi-heart</v-icon>
              <span class="subheading mr-2">{{likes}}</span>
            </a>
            <a href="#" @click.prevent="comment">
              <v-icon class="mr-1" size="x-large">mdi-comment-outline</v-icon>
              <span class="subheading">{{comments}}</span>
            </a>
          </v-row>
        </v-list-item>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: "Post",
  props:{
<<<<<<< HEAD
    id: {
      required: true,
    }
    ,
=======
>>>>>>> c566ff0ae95d99634d4da7f075ad76c891291bf6
    nickname:{
      type:String,
    },
    article:{
      type:String,
    },
    image:{
        type:String,
    },
    pic_name:{
        type:String,
        default:"no-image",
    },
    
  },
    data: function () {
      return {
          show: false,
          likes: 21,
          comments: 1,
          isLike: false,
      }
  },
  methods: {
    iLoveIt() {
      if (this.isLike) {
        this.likes -= 1;
      } else {
        this.likes += 1;
      }

      var userinfo = JSON.parse(sessionStorage.getItem('LoginUserInfo')).nickname
      console.log(userinfo)
      var form = new FormData();
      form.append('article_id', 1)
      form.append('username', userinfo)
      form.append('isLike', this.isLike)
      axios.post('http://192.168.31.87:8000/articles/like/', form)
        .then(response => {
          console.log(response)
        })
      this.isLike = !this.isLike
    },
    comment() {
      var router = this.$router
      router.push(`comment/${this.id}`)
    }
  }
}
</script>