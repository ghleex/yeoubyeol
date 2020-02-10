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
            :src="picname"
          ></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>{{ nickname }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-card-text class="subtitle-2 grey--text text--lighten-5 pb-0">
<<<<<<< HEAD
        {{ article }}
        '뭐해?'라는 두 글자에 <br>
        '네가 보고 싶어' 나의 속마음을 담아 우 <br>
        이모티콘 하나하나 속에 <br>
        달라지는 내 미묘한 심리를 알까 우 <br>
        <br>
        아니 바쁘지 않아 nothing no no <br>
        잠들어 있지 않아 insomnia nia nia <br>
        지금 다른 사람과 함께이지 않아 <br>
        응, 나도 너를 생각 중 <br>
        <br>
        우리의 네모 칸은 bloom <br>
        엄지손가락으로 장미꽃을 피워 <br>
        향기에 취할 것 같아 우 <br>
        오직 둘만의 비밀의 정원 <br>
        <br>
        I feel bloom I feel bloom I feel bloom <br>
        너에게 한 송이를 더 보내 <br>
=======
        {{article}}
>>>>>>> 7a4f844016675c21a0da49d442b5e5fe15342237
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
  // props : ['text', 'image','isLiked','picname'],
  props:{
    nickName:{
      type:String,
    },
    article:{
      type:String,
    },
    image:{
        type:String,
    },
    picName:{
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
      router.push()
    }
  }
}
</script>