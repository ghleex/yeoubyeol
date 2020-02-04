
<!--
    가입하기는 기본적인 폼만 제공됩니다
    기능명세에 따라 개발을 진행하세요.
    Sub PJT I에서는 UX, 디자인 등을 포함하여 백엔드를 제외하여 개발합니다.
 -->
<template>
    <v-card dark color="#110b22" class="my-8 d-flex align-center justify-center">
        <v-form ref="form" v-model="valid" lazy-validation class="d-flex flex-column">
            <h1 class="display-1 font-weight-black my-8">
                당신을 <br>
                기다리고 <br>
                있습니다. <br>
            </h1>
            <v-text-field
                v-model="form.nickName"
                :rules="[rules.requiredNickname, rules.validateNickname, rules.hasSpace]"
                name="nickname"
                label="별명"
                id="nickname"
                hint="영문과 숫자만 사용하여 입력해주세요."
                outlined
                dense
            ></v-text-field>
            <v-text-field
                v-model="form.email"
                :rules="[rules.requiredEmail, rules.validateEmail]"
                disabled
                name="email"
                label="이메일"
                id="email"
                outlined
                dense
            ></v-text-field>
            <v-text-field
                v-model="form.password"
                :append-icon="passwordValid ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="[rules.requiredPassword, rules.minLengthmax, rules.validatePassword, rules.hasSpace]"
                :type="passwordValid ? 'text' : 'password'"
                name="password"
                label="비밀번호"
                hint="영문, 숫자, 특수문자를 포함하여 8자 이상 입력해야합니다."
                counter
                @click:append="passwordValid = !passwordValid"
                outlined
                dense
            ></v-text-field>
            <v-text-field
                v-model="form.passwordConfirm"
                :append-icon="passwordValid ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="[rules.validateConfirm(form.password, form.passwordConfirm)]"
                :type="passwordValid ? 'text' : 'password'"
                name="passwordConfirm"
                label="비밀번호 확인"
                hint="비밀번호를 다시 한번 입력해주세요."
                counter
                @click:append="passwordValid = !passwordValid"
                outlined
                dense
            ></v-text-field>
            <v-dialog v-model="termPopup" scrollable max-width="500px">
                <template v-slot:activator="{ on }">
                    <v-checkbox
                        v-model="form.isTerm"
                        readonly
                        label="약관에 동의합니다."
                        class="mt-0"
                        v-on="on"
                    ></v-checkbox>
                </template>
                <v-card dark color="#110b15">
                    <v-card-title>개인정보 제공 및 이용약관 동의</v-card-title>
                    <v-divider></v-divider>
                    <v-card-text style="height: 300px;">
                        이용약관 내용
                    </v-card-text>
                <v-divider></v-divider>
                    <v-btn color="#71d087" class="blue-grey--text text--darken-4" @click="termAgree">동의</v-btn>
                    <v-btn @click="termDeny">취소</v-btn>
                </v-card>
            </v-dialog>
        </v-form>
        <v-btn text color="#71d087" dark :disabled="!valid" class="blue-grey--text text--darken-4 align-self-end" min-width="300px">
            <span>회원가입</span>
            <v-icon>mdi-account-check</v-icon>
        </v-btn>
        <v-alert 
            v-model="isFail"
            color="#cc6666"
            dismissible>
            회원가입 실패
        </v-alert>
        <v-alert 
            v-model="isSuccess"
            color="#71d087"
            dismissible>
            회원가입 성공
        </v-alert>
    </v-card>
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
                this.form.email = this.$store.form.email
                this.form.nickName = this.$store.form.nickName
                this.$store.form = null
            }
            this.passwordSchema
                .is().min(8)
                .is().max(20)
                .has().digits()
                .has().letters()
                .has().symbols()
                .has().not().spaces();

            let URL = document.location.href
            console.log(URL.split('/')[5].split('+'))    
            this.form.email = URL.split('/')[5].split('+')[1]
            this.form.key = URL.split('/')[5].split('+')[0]                                             
        },
        data: () => {
            return {
                // 입력된 form 데이터
                form: {
                    // 미리 입력된 데이터
                    key: '',
                    email: '',

                    // 직접 입력하도록
                    nickName: '',
                    password: '',
                    passwordConfirm: '',
                    isTerm: false,
                },

                // 비밀번호를 확인할 수 있도록 하는
                passwordValid: false,

                // 비밀번호 규칙
                passwordSchema: new PV(),

                // 요청 보낼 때 확인하기 위한 값
                error: {
                    email: null,
                    password: null,
                    nickName: null,
                    passwordConfirm: null,
                    term: null
                },

                // error의 값들이 모두 false일 경우, 버튼 활성화를 위한 값
                isSubmit: false,
                valid: false,

                // 약관 modal을 켜기 위한 스위치
                termPopup: false,

                // 회원가입 실패를 알려주기 위한 장치
                isFail: false,
                isSuccess: false,

                // 정보 입력시 유효한 데이터인지 검사
                rules: {
                    requiredNickname: value => !!value || '별명을 입력해주세요.',
                    requiredEmail: value => !!value || '이메일을 입력해주세요.',
                    requiredPassword: value => !!value || '비밀번호를 입력해주세요.',
                    emailMatch: () => ('The email and password you entered don\'t match'),
                    minLengthmax: v => (v.length >= 8 && v.length <= 20 && !/\s/.test(v)) || '비밀번호는 공백없이 8자 이상 20자 이하 입력해야합니다.',
                    validateNickname: v => !/[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/.test(v) || '한글을 제외하고 입력해주세요.',
                    validateEmail: v => /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/.test(v) || '이메일 형식을 지켜주세요.',
                    validatePassword: v => /^.*(?=^.{8,}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[`~!@#$%^&+=;',.?]).*$/.test(v) || '영문, 숫자, 특수문자를 포함하여 공백없이 입력해주세요.',
                    hasSpace: v => !/\s/.test(v) || '공백없이 입력해주세요.',
                    validateConfirm: (v1, v2) => v1 === v2  || '비밀번호가 일치하지 않습니다.'
                },
            }
        },
        methods: {
            validate() {
                if (this.$refs.form.validate()) {
                    // this.snackbar = true;
                    this.isSubmit = true;
                }
            },
            termAgree() {
                this.form.isTerm = true;
                this.termPopup = false;
            },
            termDeny() {
                this.form.isTerm = false;
                this.termPopup = false;
            },
            windowClose() {
                window.open('','_self').close();
            },
            checkForm() {
                if (!this.form.nickName) {
                    this.error.nickName = '별명을 확인해주세요.'
                    return '별명을 확인해주세요.'
                }
                else if (this.form.email && !EmailValidator.validate(this.form.email)) {
                    this.error.email = '이메일을 확인해주세요.'
                    return '이메일을 확인해주세요.'
                }
                else if (this.form.password && !this.passwordSchema.validate(this.form.password)) {
                    this.error.password = '비밀번호는 영문, 숫자, 특수문자를 포함하여 8자 이상 20자 이하여야 합니다.'
                    return '비밀번호는 영문, 숫자, 특수문자를 포함하여 8자 이상 20자 이하여야 합니다.'
                }
                else if (this.form.passwordConfirm && this.form.password !== this.form.passwordConfirm) {
                    this.error.passwordConfirm = '비밀번호가 일치하지 않습니다.'
                    return '비밀번호가 일치하지 않습니다.'
                }
                else if (!this.form.isTerm) {
                    this.error.term = '약관에 동의해야합니다.'
                    return '약관에 동의해야합니다.'
                }
                else {
                    this.error.nickName = false
                    this.error.email = false
                    this.error.password = false
                    this.error.passwordConfirm = false
                    this.error.term = false
                    return false
                }
            },
            join() {
                if (!this.error.nickName && !this.error.email && !this.error.password && !this.error.passwordConfirm && this.isTerm) {
                    let joinForm = {
                        'username': this.form.email,
                        'email': this.form.email,
                        'nickname': this.form.nickName,
                        'password': this.form.password,
                        'key': this.form.key
                    }
                    this.$store.form = joinForm
                    UserApi.requestSignup(joinForm, (response) => {
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
            // error: {
            //     deep: true,
            //     handler() {
            //         if (this.error.nickName === false && this.error.email === false && 
            //             this.error.password === false && this.error.passwordConfirm === false && this.isTerm) {
            //                 this.isSubmit = true;
            //         } else {
            //             this.isSubmit = false;
            //         }
            //     }
            // },
            form: {
                deep: true,
                handler() {
                    this.validate()
                    var check = this.checkForm()
                    if (check) {
                        console.log(check)
                    } else {
                        this.valid = true;
                    }
                }
            }
        },
    }

</script>



    <!-- <div>
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
    </div> -->



    // ---------------------------------method------------------------------------
            // checkNickname() {
            //     if (!this.nickName)
            //         this.error.nickName = '중복되거나 올바는 형식이 아닙니다.'
            //     else this.error.nickName = false;
            // },
            // checkEmail() {
            //     if (this.email && !EmailValidator.validate(this.email))
            //         this.error.email = "이메일 형식이 아닙니다."
            //     else this.error.email = false;
            // },
            // checkPassword() {
            //     if (this.password && !this.passwordSchema.validate(this.password))
            //         this.error.password = '영문,숫자 포함 8 자리이상이어야 합니다.'
            //     else
            //         this.error.password = false;
            // },
            // checkPasswordConfirm() {
            //     if (this.passwordConfirm && this.password !== this.passwordConfirm)
            //         this.error.passwordConfirm = '비밀번호가 일치하지 않습니다.'
            //     else
            //         this.error.passwordConfirm = false;
            // },
            // checkTerm() {
            //     if (this.isTerm) {
            //         this.error.term = false
            //     } else {
            //         this.error.term = true
            //     }
            // },