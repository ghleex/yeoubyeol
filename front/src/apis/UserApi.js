//가입
import axios from 'axios'
import dotenv from 'dotenv';

dotenv.config();
const requestSignup = (data, callback, errorCallback) => {
    console.log(data);
    //백앤드와 로그인 통신하는 부분
    let form = new FormData()
    form.append('nickname', data.nickname)
    form.append('username', data.email)
    form.append('password', data.password)
    axios.post(`http://${process.env.VUE_APP_IP}/accounts/signup/${data.key}/`, form)
        .then((response) => {
            console.log(response)
            callback(response)

        })
        .catch((response) => {
            console.log(response)
            console.log('catch ' + response)
            errorCallback('error')
        })
}

//로그인
const requestLogin = (data, callback, errorCallback) => {
    // console.log(data)
    let credentials = {
        username: data.email,
        password: data.password,
    }

    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

    axios.post(`http://${process.env.VUE_APP_IP}/auth/`, credentials)
        .then(res => {
            // console.log(res)
            // this.$store.dispatch('login', res.data.token)
            console.log('로그인 성공')
            callback(res)
        })
        .catch(err => {
            console.log('로그인 에러')
            errorCallback('error')
        })
}

// 로그인 체크 data = token
const requestLoginCheck = (data, callback, errorcallback) => {

    axios.post(`http://${process.env.VUE_APP_IP}/accounts/check/`, data)
        .then(response => {
            console.log(response)
            callback(response.data.token_2)
        })
        .catch(error => {
            console.log(error)
            errorcallback(error)
    })
}

//회원프로필가져올래
const requestUserProfile = (data, callback, errorCallback) => {
    let nickname = {
        nickname: data,
    }
    // console.log(nickname)
    axios.post(`http://${process.env.VUE_APP_IP}/accounts/profile/`, nickname)
        .then(res => {
            // console.log(res)
            // this.$store.dispatch('login', res.data.token)
            console.log('프로필 조회 성공')
            callback(res)
        })
        .catch(err => {
            console.log(err)
            errorCallback()
        })
}

//팔로워 목록 받아오기
const requestFollowers= (data, callback, errorCallback) => {
    let nickname = {
        nickname: data,
    }
    // console.log(nickname)
    axios.post(`http://${process.env.VUE_APP_IP}/articles/followerlist/`, nickname)
        .then(res => {
            console.log('팔로워리스트 가져오기 성공')
            callback(res)
        })
        .catch(err => {
            console.log('팔로워리스트 가져오기 시루패 ㅜ')
            console.log(err)
            errorCallback(err)
        })
}
//팔로잉 목록 받아오기
const requestFollowings= (data, callback, errorCallback) => {
    let nickname = {
        nickname: data,
    }
    // console.log(nickname)
    axios.post(`http://${process.env.VUE_APP_IP}/articles/following/`, nickname)
        .then(res => {
            console.log('팔로잉리스트 가져오기 성공')
            callback(res)
        })
        .catch(err => {
            console.log('팔로잉리스트 가져오기 시루패 ㅜ')
            console.log(err)
            errorCallback(err)
        })
}


const UserApi = {
    requestSignup: (data, callback, errorCallback) => requestSignup(data, callback, errorCallback),
    requestLogin: (data, callback, errorCallback) => requestLogin(data, callback, errorCallback),
    requestUserProfile: (data, callback, errorCallback) => requestUserProfile(data, callback, errorCallback),
    requestFollowers: (data, callback, errorCallback) => requestFollowers(data, callback, errorCallback),
    requestFollowings: (data, callback, errorCallback) => requestFollowings(data, callback, errorCallback),
    requestLoginCheck: (data, callback, errorCallback) => requestLoginCheck(data, callback, errorCallback),
}
export default UserApi