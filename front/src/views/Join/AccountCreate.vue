
<!--
    가입하기는 기본적인 폼만 제공됩니다
    기능명세에 따라 개발을 진행하세요.
    Sub PJT I에서는 UX, 디자인 등을 포함하여 백엔드를 제외하여 개발합니다.
 -->
<template>
    <div>
        <div class="wrapC">
            <h1>
                당신을 <br>
                기다리고 있습니다. <br>
            </h1>
            <div>
                <div class="join">
                    <label for="nickname">닉네임</label>
                    <input v-model="nickName"
                        :class = "{error : error.nickName, complete: !error.nickName&&nickName.length !== 0}"
                        id="nickname"
                        placeholder="닉네임을 입력하세요." type="text"/>
                    <div class="error-text" v-if="error.nickName">
                        {{error.nickName}}
                    </div>
                </div>

                <div class="join">
                    <label for="email">이메일</label>
                    <input v-model="email" 
                        disabled
                        :class="{error : error.email, complete:!error.email&&email.length!==0}"
                        id="email" placeholder="이메일을 입력하세요."
                        type="text"/>
                    <div class="error-text" v-if="error.email">
                        {{error.email}}
                    </div>
                </div>

                <div class="join">
                    <label for="password">비밀번호</label>
                    <input v-model="password"
                        v-bind:class="{error : error.password, complete:!error.password&&password.length!==0}"
                        id="password" :type="passwordType"
                        placeholder="비밀번호를 입력하세요."/>
                    <div class="error-text" v-if="error.password">
                        {{error.password}}
                    </div>
                </div>

                <div class="join">
                    <label for="password-confirm">비밀번호 확인</label>
                    <input v-model="passwordConfirm" :type="passwordConfirmType"
                        v-bind:class="{error : error.passwordConfirm, complete:!error.passwordConfirm&&passwordConfirm.length!==0&&password===passwordConfirm}"
                        id="password-confirm"
                        placeholder="비밀번호를 다시한번 입력하세요."/>
                    <div class="error-text" v-if="error.passwordConfirm">
                        {{error.passwordConfirm}}
                    </div>
                </div>
            </div>
            <div class="policy">
                <label>
                    <input v-model="isTerm" type="checkbox" id="term"/>
                    <span>약관을 동의합니다.</span>
                </label>
                <span class="popup" @click="termPopup=true">약관보기</span>

            </div>
            <div class="flex-column-end">
                <button @click.prevent="join" class="base confirm" :class="{notallowed: !isSubmit}">
                    함께하기
                </button>
            </div>
        </div>
        <div v-if="isFail" style="display: flex; justify-content: center; align-items: center; background-color: red; position: absolute; bottom: 0; width: 100%; height: 50px;">
            <p>{{ isFail }}</p>
        </div>
        <div v-if="isSuccess" style="display: flex; justify-content: center; align-items: center; background-color: #2fd45d; position: absolute; bottom: 0; width: 100%; height: 50px;">
            <p>{{ isSuccess }}</p>
        </div>
    </div>
</template>

<script>
    import '../../assets/css/style.scss'
    import '../../assets/css/user.scss'
    import PV from 'password-validator'
    import * as EmailValidator from 'email-validator';
    import UserApi from '../../apis/UserApi'
    export default {
        created(){
            if (this.$store.form) {
                this.email = this.$store.form.email
                this.nickName = this.$store.form.nickName
                this.$store.form = null
            }
            this.passwordSchema
                .is().min(8)
                .is().max(100)
                .has().digits()
                .has().letters()
                .has().symbols()
                .has().not().spaces();
            let URL = document.location.href
            console.log(URL.split('/')[5].split('+'))    
            this.email = URL.split('/')[5].split('+')[1]
            this.key = URL.split('/')[5].split('+')[0]                                             
        },
        data: () => {
            return {
                key: '',
                email: '',
                password: '',
                passwordConfirm: '',
                passwordSchema: new PV(),
                nickName: '',
                isTerm: false,
                isLoading: false,
                error: {
                    email: null,
                    password: null,
                    nickName: null,
                    passwordConfirm: null,
                    term: null
                },
                isSubmit: false,
                passwordType: "password",
                passwordConfirmType: "password",
                termPopup: false,
                isFail: false,
                isSuccess: false,
            }
        },
        methods: {
            windowClose() {
                window.open('','_self').close();
            },
            checkNickname() {
                if (!this.nickName)
                    this.error.nickName = '중복되거나 올바는 형식이 아닙니다.'
                else this.error.nickName = false;
            },
            checkEmail() {
                if (this.email && !EmailValidator.validate(this.email))
                    this.error.email = "이메일 형식이 아닙니다."
                else this.error.email = false;
            },
            checkPassword() {
                if (this.password && !this.passwordSchema.validate(this.password))
                    this.error.password = '영문,숫자 포함 8 자리이상이어야 합니다.'
                else
                    this.error.password = false;
            },
            checkPasswordConfirm() {
                if (this.passwordConfirm && this.password !== this.passwordConfirm)
                    this.error.passwordConfirm = '비밀번호가 일치하지 않습니다.'
                else
                    this.error.passwordConfirm = false;
            },
            checkTerm() {
                if (this.isTerm) {
                    this.error.term = false
                } else {
                    this.error.term = true
                }
            },
            join() {
                if (!this.error.nickName && !this.error.email && !this.error.password && !this.error.passwordConfirm && this.isTerm) {
                    let tmp = {
                        'username': this.email,
                        'email': this.email,
                        'nickname': this.nickName,
                        'password': this.password,
                        'key': this.key
                    }
                    this.$store.form = tmp
                    UserApi.requestSignup(tmp, (response) => {
                        console.log('-----response-----')
                        console.log(response)
                        this.isSuccess = response.data.message
                        setTimeout(() => {
                            this.isSuccess = false;
                            this.windowClose();
                        }, 2000)
                    },
                    error => {
                        console.log('회원가입 실패!')
                        this.isFail = '회원가입 실패'
                        setTimeout(() => {
                            this.isFail = false
                        }, 2000)
                    })
                    //----------------------------------------
                    // 회원가입을 위해 back으로 추가정보 전송
                    // var router = this.$router
                    // router.push({name: '이메일 인증'})
                    //----------------------------------------
                } else if (this.error.nickName) {
                    alert('닉네임을 다시 확인해주세요.')
                } else if (this.error.email) {
                    alert('이메일을 다시 확인해주세요.')
                } else if (this.error.password || this.error.passwordConfirm) {
                    alert('비밀번호를 다시 확인해주세요.')
                } else if (!this.isTerm) {
                    alert('약관에 동의해주세요.')
                }
            }
        },
        watch: {
            nickName: function(v) {
                this.checkNickname();
            },
            email: function(v) {
                this.checkEmail();
            },
            password: function(v) {
                this.checkPassword();
                this.checkPasswordConfirm();
            },
            passwordConfirm: function(v) {
                this.checkPasswordConfirm();
            },
            isTerm: function(v) {
                this.checkTerm();
            },
            error: {
                deep: true,
                handler() {
                    if (this.error.nickName === false && this.error.email === false && 
                        this.error.password === false && this.error.passwordConfirm === false && this.isTerm) {
                        this.isSubmit = true;
                    } else {
                        this.isSubmit = false;
                    }
                }
            },
        },
    }

</script>


