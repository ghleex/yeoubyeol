<template>
  <div>
    <Post />
  </div>
</template>

<script>
import Post from '@/components/common/Post'

export default {
  components: {
    Post,
  },
  created(){
    // if (!this.$cookies.isKey('auth_cookie')){
    //   alert('로그인이 필요한 서비스에요')
    //   this.$router.push({path:'/'});

    // }
  }

}
</script>
