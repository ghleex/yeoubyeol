//follow 친구 맺기 /끊기 
import axios from 'axios'
const requestFollow = (data, callback, errorCallback) => {
    console.log(data);
    //백앤드와 로그인 통신하는 부분
    let form = new FormData()
    form.append('my_nickname', data.loginedNickname)
    form.append('your_nickname', data.shownNickname)
    axios.post(`http://192.168.31.80:8000/articles/follow`, form)
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


const FeedApi = {
    requestFollow: (data, callback, errorCallback) => requestFollow(data, callback, errorCallback),
}
export default FeedApi