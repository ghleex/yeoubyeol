//follow 친구 맺기 /끊기 
const ip ="http://192.168.31.87:8000"; 

import axios from 'axios'
const requestFollow = (data, callback, errorCallback) => {
    console.log(data);
    let form = new FormData()
    form.append('my_nickname', data.loginedNickname)
    form.append('your_nickname', data.shownNickname)
    axios.post(`${ip}/articles/follower/`, form)
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
const newPost = (form, callback, errorCallback) => {
    

     axios.post(`${ip}/articles/`, form,{
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

//해시태그 추천받기
const requestHashTags = (form, callback, errorCallback) => {
    

     axios.post(`${ip}/articles/recommend/`, form,{
     })
        .then((response) => {
            console.log('해시태그 받기 성공 :',response)
            callback(response)
        
        })
        .catch((response) => {
            console.log(response)
            console.log('해시태그 받기 오류'  + response)
            errorCallback('error')
        }) 
}

//게시글 가져오기
const getArticles = (data, callback, errorCallback) => {
    let form = new FormData()
    form.append('nickname', data)
    axios.post(`${ip}/articles/mainfeed/`, form,{
    })
       .then((response) => {
           console.log('게시글 받기 성공 :',response)
           callback(response)
       
       })
       .catch((response) => {
           console.log(response)
           console.log('게시글 받기 오류'  + response)
           errorCallback('error')
       }) 
}

//게시글 가져오기 : 아이디로 조회하기
const getArticleById = (data, callback, errorCallback) => {
    axios.get(`${ip}/articles/${data}/`,{
    })
       .then((response) => {
           console.log('게시글 받기 성공 :',response)
           callback(response)
       
       })
       .catch((response) => {
           console.log(response)
           console.log('게시글 받기 오류'  + response)
           errorCallback('error')
       }) 
}


const FeedApi = {
    requestFollow: (data, callback, errorCallback) => requestFollow(data, callback, errorCallback),
    newPost: (data, callback, errorCallback) => newPost(data, callback, errorCallback),
    requestHashTags: (data, callback, errorCallback) => requestHashTags(data, callback, errorCallback),
    getArticles: (data, callback, errorCallback) => getArticles(data, callback, errorCallback),
    getArticleById: (data, callback, errorCallback) => getArticleById(data, callback, errorCallback),
}
export default FeedApi