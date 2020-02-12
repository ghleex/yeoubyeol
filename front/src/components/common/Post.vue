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
          {{ timedelta }}
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
import dotenv from 'dotenv';

dotenv.config();
export default {
  name: "Post",
  props:{
    id: {
      required: true,
    }
    ,
    nickname:{
      type: String,
    },
    article:{
      type: String,
    },
    image:{
      type: String,
    },
    pic_name:{
      type: String,
      default: "no-image",
    },
    comments: {
      type: Number
    },
    likes: {
      type: Number
    },
    created_at: {
      type: String
    }
  },
    data: function () {
      return {
          show: false,
          isLike: false,
          timedelta: '',
      }
  },
  created() {
    let date = new Date();
    let maybe = new Date(this.created_at)
    let diffTime = Math.ceil((date - maybe) / 1000 / 60 / 60 )

    if (diffTime < 30) {
      this.timedelta = '조금 전'
    } else if (diffTime < 24) {
      this.timedelta = `${diffTime}시간 전`
    } else {
      this.timedelta = `${date.getDate() - maybe.getDate()}일 전`
    }
  },
  methods: {
    iLoveIt() {
      var userinfo = JSON.parse(sessionStorage.getItem('LoginUserInfo')).nickname
      console.log(userinfo)
      var form = new FormData();
      form.append('article_id', 1)
      form.append('username', userinfo)
      form.append('isLike', this.isLike)
      axios.post(`http://${process.env.VUE_APP_IP}/articles/like/`, form)
        .then(response => {
          console.log(response)
        })
      this.isLike = !this.isLike
    },
    comment() {
      var router = this.$router
      router.push(`feed/${this.id}`)
    }
  }
}
</script>