//follow 친구 맺기 /끊기 
import axios from 'axios'
const requestFollow = (data, callback, errorCallback) => {
    console.log(data);
    let form = new FormData()
    form.append('my_nickname', data.loginedNickname)
    form.append('your_nickname', data.shownNickname)
    axios.post(`http://192.168.31.87:8000/articles/follower/`, form)
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

//새 글 작성하기
const newPost = (data, callback, errorCallback) => {
    console.log(data)
     axios.post(`http://192.168.31.87:8000/articles/`, data,{
        headers: {
            'Content-Type': 'multipart/form-data',
        }
     })
        .then((response) => {
            console.log('글작성 :',response)
            callback(response)
        
        })
        .catch((response) => {
            console.log(response)
            console.log('글작성 오류'  + response)
            errorCallback('error')
        }) 
}


const FeedApi = {
    requestFollow: (data, callback, errorCallback) => requestFollow(data, callback, errorCallback),
    newPost: (data, callback, errorCallback) => newPost(data, callback, errorCallback),
}
export default FeedApi