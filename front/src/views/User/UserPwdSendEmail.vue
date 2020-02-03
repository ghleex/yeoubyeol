<template>
    <div class="wrapC">
        <h1>
            가입할 때 사용하신 <br>
            이메일로 변경링크를 <br>
            보내드릴게요.
        </h1>
        <div class="email-input">
            <form action="" class="flex-center">
                <div>
                    <input
                        v-model="email" v-bind:class="{error : error.email, complete:!error.email&&email.length!==0}"
                        placeholder="이메일을 입력해주세요" label="이메일" maxLength="100"
                    />
                    <div class="error-text" v-if="error.email">
                        {{error.email}}
                    </div>
                </div>
                <div>
                    <button class="orange confirm" @click.prevent="sendEmail"
                            :class="{notallowed: !isSubmit}"
                    >이메일 전송</button>
                </div>
                
            </form>
        </div>
    </div>
</template>

<script>
    // import ButtonCustom from '../../components/common/ButtonCustom'
    import emailjs from 'emailjs-com';
    import * as EmailValidator from 'email-validator';
    import axios from 'axios';
    export default {
        components: {
            // ButtonCustom,
        },
        created() {
            if (this.$store.email) {
                this.email = this.$store.email
                if (this.checkForm()) {
                    this.isSubmit = true
                }
                this.$store.email = null
            }
        },
        data: () => {
            return {
                email: '',
                error: {
                    email: false,
                },
                isSubmit: false,
            }
        },
        methods: {
            checkForm() {
                if (this.email.length >= 0 && !EmailValidator.validate(this.email)) {
                    this.error.email = "이메일 형식이 아닙니다."
                    console.log('hi')
                    return false
                } else {
                    this.error.email = false;
                    console.log('bye')
                    return true
                }
            },
            sendEmail() {
                var router = this.$router
                console.log(this.email)
                if (this.email && !this.error.email) {
                    this.$store.email = this.email
                    router.push({
                        path: '/user/password/ok'
                    })
                let form = new FormData();
                form.append('username', this.email)
                axios.post('http://192.168.31.80:8000/accounts/find_pwd/', form)
                .then(response => {
                    console.log(response)
                })
                }
            },
        },
        watch: {
            email: function (v) {
                this.checkForm();
            },
            error: {
                deep: true,
                handler() {
                    if (!this.error.email) {
                        this.isSubmit = true
                    } else {
                        this.isSubmit = false
                    }
                }
            }
        },

    }
</script>