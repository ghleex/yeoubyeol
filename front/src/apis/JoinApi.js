//가입
import axios from 'axios'
import dotenv from 'dotenv';

dotenv.config();
//회원프로필가져올래
const JoinsendEmail = (data, callback, errorCallback) => {
    let form = new FormData();
        form.append("username", data);

    // console.log(nickname)
    axios.post(`${process.env.VUE_APP_IP}/accounts/email/`, form)
        .then(res => {
            console.log('메일보내깅 신청 성공')
            callback(res)
            //todo
            //이미있는 이메일에대한 요청에 대한 처리 필요
        })
        .catch(err => {
            console.log('메일보내기 에러')
            errorCallback(err);
        })
}

const sendEmailPW = (data, callback, errorCallback) => {
    let form = new FormData();
        form.append("username", data);

    // console.log(nickname)
    axios.post(`${process.env.VUE_APP_IP}/accounts/find_pwd/`, form)
        .then(res => {
            console.log('비번찾기 메일보내깅 신청 성공')
            callback(res)
            //todo
            //이미있는 이메일에대한 요청에 대한 처리 필요
        })
        .catch(err => {
            console.log('비번찾기 메일보내기 에러')
            errorCallback(err);
        })
}


const JoinApi = {
    JoinsendEmail: (data, callback, errorCallback) => JoinsendEmail(data, callback, errorCallback),
    sendEmailPW: (data, callback, errorCallback) => sendEmailPW(data, callback, errorCallback)
}
export default JoinApi