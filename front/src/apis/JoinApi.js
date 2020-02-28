//가입
import axios from 'axios'
import dotenv from 'dotenv';

dotenv.config();

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

//회원프로필가져올래
const JoinsendEmail = (data, callback, errorCallback) => {
    let form = new FormData();
        form.append("username", data);

    axios.post(`${process.env.VUE_APP_IP}/accounts/email/`, form)
        .then(res => {
            callback(res)
            //todo
        })
        .catch(err => {
            errorCallback(err);
        })
}

const sendEmailPW = (data, callback, errorCallback) => {
    let form = new FormData();
        form.append("username", data);

    axios.post(`${process.env.VUE_APP_IP}/accounts/findpwd/`, form)
        .then(res => {
            callback(res)
            //todo
            //이미있는 이메일에대한 요청에 대한 처리 필요
        })
        .catch(err => {
            errorCallback(err);
        })
}


const JoinApi = {
    JoinsendEmail: (data, callback, errorCallback) => JoinsendEmail(data, callback, errorCallback),
    sendEmailPW: (data, callback, errorCallback) => sendEmailPW(data, callback, errorCallback)
}
export default JoinApi