<template>
  <div>
    <Post />
  </div>
</template>

<script>
import Post from '@/components/common/Post';
import axios from 'axios'

export default {
  components: {
    Post,
  },
  created(){
    axios.get('http://192.168.31.87:8000/articles/')
      .then(response => {
        console.log(response.data);
        this.articles = response.data;
      })
    // if (!this.$cookies.isKey('auth_cookie')){
    //   alert('로그인이 필요한 서비스에요')
    //   this.$router.push({path:'/'});

    // }
  },
  data:() => {
    return {
      articles: null,
    }
  }

}
</script>
