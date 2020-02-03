<template>
  <div class="wrapC flex-center">
    <div>
      <h1 style="color: #FFFFFF;">
        변경할 비밀번호를 입력해주세요.
      </h1>
       <br>
      <h3 style="color: #71D087;">
        | 영문, 숫자를 포함하여 8자 이상 입력해주세요.
      </h3>
      <br>
      <form action="" class="flex-center" @submit.prevent="changePwd">
        <div>
          <input type="password" v-model="password"
            style="background-color: #ffffff; width: 100%; color: #71D087;" placeholder="새로운 비밀번호를 입력해주세요.">
          <p v-if="error" style="color: #EF3939;">{{ error }}</p>
        </div>
        <button
          style="border: 1px solid #71D087; 
                 color: #71D087; 
                 width: 100%; 
                 height: 50px; 
                 margin: 15px 0;
                 font-size: 16px;
                 font-weight: bold;
                 border-radius: 5px;"
        >비밀번호 변경</button>
      </form>
    </div>
  </div>
</template>

<script>
import '../../assets/css/common.scss'
import '../../assets/css/style.scss'
import PV from 'password-validator'
export default {
  created() {
    this.passwordSchema
      .is().min(8)
      .is().max(100)
      .has().digits()
      .has().letters()
      .has().symbols()
      .has().not().spaces();
  },
  data: () => {
    return {
      isSubmit: false,
      passwordSchema: new PV(),
      password: '',
      error: false
    }
  },
  watch: {
    password: function() {
      this.checkPwd()
    }
  },
  methods: {
    changePwd() {
      if (this.isSubmit) {
        alert('비밀번호가 변경되었습니다.')
      } else {
        alert('다시 확인해주세요.')
      }
    },
    checkPwd() {
      if (this.password && !this.passwordSchema.validate(this.password)) {
        this.error = '영문,숫자 포함 8 자리이상이어야 합니다.'
        this.isSubmit = false
      } else if (this.password && this.passwordSchema.validate(this.password)) {
        this.error = false
        this.isSubmit = true
      }
    }
  }
}
</script>

<style>

</style>